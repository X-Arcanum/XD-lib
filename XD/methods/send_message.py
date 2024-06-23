import requests
import json
from parse import parse_buttons
class TelegramMessage:
    def __init__(self, bot, chat_id, text, thread_id=None, parse_mode=None, entities=None, disable_preview=None, disable_notification=None, content_protection=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None, **kwargs):
        self.bot = bot
        self.chat_id = chat_id
        self.text = text
        self.thread_id = thread_id
        self.parse_mode = parse_mode
        self.entities = entities
        self.disable_preview = disable_preview
        self.content_protection = content_protection
        self.reply_to_message_id = reply_to_message_id
        self.allow_sending_without_reply = allow_sending_without_reply
        self.reply_markup = reply_markup
        self.extra = kwargs

class TelegramBot:
    def __init__(self, bot_token, bot_url):
        self.bot_token = bot_token
        self.bot_url = bot_url

    def send_message(self, chat_id, text, message_thread_id=None, parse_mode=None, entities=None, disable_web_page_preview=None, protect_content=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None, **kwargs):
        url = f"{self.bot_url}/sendMessage?chat_id={chat_id}&text={text}"
        if message_thread_id:
            url += f"&message_thread_id={message_thread_id}"
        if parse_mode:
            url += f"&parse_mode={parse_mode}"
        if entities:
            url += f"&entities={entities}"
        if disable_web_page_preview:
            url += f"&disable_web_page_preview={disable_web_page_preview}"
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

