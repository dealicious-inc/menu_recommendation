from bs4 import BeautifulSoup


class SlackMessageFormatter:
    def restaurant_info_format(self, order_depth_1, order_depth_2, title, restaurant_info):
        block = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{self._title_number(order_depth_1, order_depth_2)} {title}",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{restaurant_info['routeUrl']}|{restaurant_info['name']}>* | {restaurant_info['category']}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"📍 주소: {restaurant_info['roadAddress']}\n\n"
                            f"📌 카테고리: {restaurant_info['category']}\n\n"
                            f"💰 가격대: {restaurant_info['priceCategory']}\n\n"
                            f"⭐ 평점: {self.star_pattern(float(restaurant_info['visitorReviewScore']))} ({restaurant_info['visitorReviewScore']})\n\n"
                            f"💾 즐겨찾기: {restaurant_info['saveCount']}명 저장\n\n"
                            f"✏️ 리뷰 수: {restaurant_info['visitorReviewCount']}개"
                },
                "accessory": {
                    "type": "image",
                    "image_url": restaurant_info['imageUrl'],
                    "alt_text": "restaurant image"
                }
            }
        ]

        if restaurant_info['review']:
            block.append({"type": "divider"})
            reviews = "\n".join(
                [f"{self.number_emoji(i + 1)} {self.clean_html(review)}\n\n" for i, review in
                 enumerate(restaurant_info['review'])])
            block.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"📝 *리뷰*\n\n{reviews}"}
            })

        # 가독성을 위해 공백 추가
        block.append({"type": "section", "text": {"type": "mrkdwn", "text": "\n"}})
        block.append({"type": "section", "text": {"type": "mrkdwn", "text": "\n"}})

        return block

    @staticmethod
    def star_pattern(score):
        if score == 0:
            return "없음"

        full_stars = int(score)
        return "⭐" * full_stars

    def _title_number(self, n, m):
        return f"{self.number_finger_emoji(n)} - {self.number_emoji(m)}"

    @staticmethod
    def number_emoji(n):
        emoji_dict = {
            1: ":one:",
            2: ":two:",
            3: ":three:",
            4: ":four:",
            5: ":five:",
            6: ":six:",
            7: ":seven:",
            8: ":eight:",
            9: ":nine:",
            10: ":keycap_ten:"
        }
        return emoji_dict.get(n, ":question:")

    @staticmethod
    def number_finger_emoji(n):
        emoji_dict = {
            1: ":point_up:",
            2: ":v:",
            3: ":i_love_you_hand_sign:",
        }
        return emoji_dict.get(n, ":question:")

    @staticmethod
    def clean_html(raw_html):
        """HTML 태그를 제거하고 깨끗한 텍스트만 반환"""
        return BeautifulSoup(raw_html, "html.parser").get_text()




