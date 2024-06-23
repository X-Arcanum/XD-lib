import requests

class TelegramBot:
    def __init__(self, bot_token, bot_url):
        self.bot_token = bot_token
        self.bot_url = bot_url

    def get_me(self):
        url = f"{self.bot_url}/getMe"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('result')
        else:
            return None

