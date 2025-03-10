from slack_notifier import SlackNotifier
from slack_message_formatter import SlackMessageFormatter
from restaurant_info_fetcher import RestaurantInfoFetcher

if __name__ == "__main__":

    slack_notifier = SlackNotifier()
    slack_message_formatter = SlackMessageFormatter()

    # 슬랙 대표 메시지 전송
    response = slack_notifier.send_main_message("🍔🥗🍣 오늘 점심으로 뭘 먹을까요? 🍔🥗🍣")
    thread_ts = response.get("ts")

    # search options에 해당하는 음식점 정보를 가져와서 슬랙에 전송
    search_options = [
        {"title": "요즘뜨는 신상맛집", "rank": '요즘뜨는', "keyword_filter": "filterOpening^true", "pick_count": 1},
        {"title": "특별한 메뉴로 많은 사람들에게 인기있는 맛집", "rank": '많이찾는', "keyword_filter": "voting^28", "pick_count": 1},
        {"title": "많은 리뷰로 검증된 맛집", "rank": '리뷰많은', "keyword_filter": None, "pick_count": 3},
    ]

    restaurant_info_fetcher = RestaurantInfoFetcher()
    for order_depth_1, search_option in enumerate(search_options, start=1):
        restaurant_infos = restaurant_info_fetcher.get_restaurant_info(search_option)
        if restaurant_infos:
            for order_depth_2, restaurant_info in enumerate(restaurant_infos, start=1):
                block = slack_message_formatter.restaurant_info_format(order_depth_1, order_depth_2, search_option['title'], restaurant_info)
                slack_notifier.send_thread_message(search_option['title'], block, thread_ts)