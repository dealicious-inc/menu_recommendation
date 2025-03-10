import requests
import json
import random
from naver_map_api import NaverMapAPI


class RestaurantInfoFetcher:
    def get_restaurant_info(self, search_options):
        try:
            response = NaverMapAPI(search_options).post()
            restaurants = response.json()[0]['data']['restaurants']['items']
            picked_restaurants = self.pick_k_restaurants(restaurants, search_options['pick_count'])

            return [self.format_restaurant_info(restaurant) for restaurant in picked_restaurants]
        except Exception as e:
            print(f"An error occurred in getting restaurant info: {e}")
            return []

    @staticmethod
    def format_restaurant_info(restaurant):
        """
        음식점 정보를 원하는 형태로 가공
        """
        return {
            "name": restaurant.get("name") or "알 수 없음",  # 가게 이름
            "category": restaurant.get("category") or "카테고리 없음",  # 카테고리
            "roadAddress": restaurant.get("roadAddress") or "주소 없음",  # 주소
            "distance": restaurant.get("distance") or "거리 없음",  # 거리 (현재 위치로부터 미터 단위)
            "imageUrl": restaurant.get("imageUrl") or "이미지 없음",  # 이미지 url
            "routeUrl": restaurant.get("routeUrl") or "경로 없음",  # 가는 경로 url
            "priceCategory": restaurant.get("priceCategory") or "없음",  # 가격대
            "saveCount": restaurant.get("saveCount") or 0,  # 네이버 저장수
            "visitorReviewScore": restaurant.get("visitorReviewScore") or 0,  # 평점
            "visitorReviewCount": restaurant.get("visitorReviewCount") or 0,  # 리뷰 수
            "review": [review.get("review", "리뷰 없음") for review in
                       restaurant.get("visitorReviews", [{}])[:3]]  # 리뷰 정보
        }

    @staticmethod
    def pick_k_restaurants(restaurants, k):
        """
        랜덤으로 k개의 음식점을 선택(단, 카페는 제외)
        """
        restaurants = [restaurant for restaurant in restaurants if '카페' not in restaurant.get('category', '')]

        if len(restaurants) < k:
            return restaurants
        return random.sample(restaurants, k)

