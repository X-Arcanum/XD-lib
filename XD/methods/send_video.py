import requests
import json
from parse import parse_buttons

class TelegramBot:
    def __init__(self, bot_token, bot_url):
        self.bot_token = bot_token
        self.bot_url = bot_url

    def send_video(self, chat_id, video, message_thread_id=None, duration=None, width=None, height=None, caption=None, parse_mode=None, caption_entities=None, supports_streaming=None, disable_notification=None, protect_content=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None, **kwargs):
        url = f"{self.bot_url}/sendVideo?chat_id={chat_id}&video={video}"
        if message_thread_id:
            url += f"&message_thread_id={message_thread_id}"
        if duration:
            url += f"&duration={duration}"
        if width:
            url += f"&width={width}"
        if height:
            url += f"&height={height}"
        if caption:
            url += f"&caption={caption}"
        if parse_mode:
            url += f"&parse_mode={parse_mode}"
        if caption_entities:
            url += f"&caption_entities={caption_entities}"
        if supports_streaming:
            url += f"&supports_streaming={supports_streaming}"
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
            return None
        else:
            return response.json().get('result')
