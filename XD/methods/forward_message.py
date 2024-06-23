import requests

class TelegramBot:
    def __init__(self, bot_token, bot_url):
        self.bot_token = bot_token
        self.bot_url = bot_url

    def forward_message(self, chat_id, from_chat_id, message_id, message_thread_id=None, disable_notification=None, protect_content=None, **kwargs):
        url = f"{self.bot_url}/forwardMessage?chat_id={chat_id}&from_chat_id={from_chat_id}&message_id={message_id}"
        if message_thread_id:
            url += f"&message_thread_id={message_thread_id}"
        if disable_notification:
            url += f"&disable_notification={disable_notification}"
        if protect_content:
            url += f"&protect_content={protect_content}"

        response = requests.get(url, params=kwargs)
        if response.status_code != 200:
            return None
        else:
            return response.json().get('result')
