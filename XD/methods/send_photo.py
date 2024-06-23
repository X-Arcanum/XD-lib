import requests
import json
from parse import parse_buttons

class TelegramBot:
    def __init__(self, bot_token, bot_url):
        self.bot_token = bot_token
        self.bot_url = bot_url

    def send_photo(self, chat_id, photo, message_thread_id=None, caption=None, parse_mode=None, caption_entities=None, disable_notification=None, protect_content=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None, **kwargs):
        url = f"{self.bot_url}/sendPhoto?chat_id={chat_id}&photo={photo}"
        if message_thread_id:
            url += f"&message_thread_id={message_thread_id}"
        if caption:
            url += f"&caption={caption}"
        if parse_mode:
            url += f"&parse_mode={parse_mode}"
        if caption_entities:
            url += f"&caption_entities={caption_entities}"
        if disable_notification:
            url += f"&disable_notification={disable_notification}"
        if protect_content:
            url += f"&protect_content={protect_content}"
        if reply_to_message_id:
            url += f"&reply_to_message_id={reply_to_message_id}"
        if allow_sending_without_reply:
            url += f"&allow_sending_without_reply={allow_sending_without_reply}"
        if reply_markup:
            btns = parse_buttons(reply_markup)
            btns = json.dumps(btns)
            url += f"&reply_markup={btns}"

        response = requests.get(url, params=kwargs)
        if response.status_code != 200:
            # Handle error or raise an exception
            return None
        else:
            return response.json().get('result')

