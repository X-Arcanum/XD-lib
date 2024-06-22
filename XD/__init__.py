import requests
import asyncio
import logging
from functools import wraps
from .exceptions import UnAuthorizedBotToken, UnKnownError, ChatNotFound, ConversationTimeOut


class TelegramMessage:
    def __init__(self, message_data, bot):
        self.data = message_data
        self.chat = self.Chat(message_data['chat'])
        self.from_user = self.FromUser(message_data['from'])
        self.bot = bot

    class Chat:
        def __init__(self, chat_data):
            self.id = chat_data['id']

    class FromUser:
        def __init__(self, from_data):
            self.id = from_data['id']
            self.first_name = from_data.get('first_name')
            self.last_name = from_data.get('last_name')
            self.username = from_data.get('username')

    async def reply_text(self, text, parse_mode='MARKDOWN'):
        return await self.bot.send_message(self.chat.id, text, parse_mode, self.data['message_id'])

    async def reply_photo(self, photo, caption=None):
        return await self.bot.send_photo(self.chat.id, photo, caption, self.data['message_id'])
    
    async def reply_audio(self, audio):
        return await self.bot.send_audio(self.chat.id, audio, self.data['message_id'])

    async def reply_document(self, document):
        return await self.bot.send_document(self.chat.id, document, self.data['message_id'])

    async def reply_video(self, video):
        return await self.bot.send_video(self.chat.id, video, self.data['message_id'])

    async def reply_voice(self, voice):
        return await self.bot.send_voice(self.chat.id, voice, self.data['message_id'])            


class Client:
    def __init__(self, token):
        if len(token) != 46:
            raise ValueError("Invalid bot token length. Bot token must be 46 characters long.")
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        self._message_handlers = {}
        self.session = requests.Session()

    def _setup_logging(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def validate_token(self):
        try:
            response = self.session.get(f"{self.base_url}/getMe")
            if response.status_code == 200:
                bot_info = response.json()['result']
                self.logger.info("Bot token is valid.")
                return True
            elif response.status_code == 401:
                raise UnAuthorizedBotToken(self.token)
            else:
                raise UnKnownError(response.status_code)
        except Exception as e:
            self.logger.error(f"Exception occurred while validating bot token: {e}")
            return False

    async def _send_request(self, method, data):
        try:
            response = requests.post(f"{self.base_url}/{method}", data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to send {method} request. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception occurred while sending {method} request: {e}")
            return None

    async def send_message(self, chat_id, text, parse_mode='MARKDOWN', reply_to_message_id=None):
        data = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendMessage', data)

    async def send_audio(self, chat_id, audio, reply_to_message_id=None):
        data = {'chat_id': chat_id, 'audio': audio}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendAudio', data)

    async def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None):
        data = {'chat_id': chat_id, 'photo': photo, 'caption': caption}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendPhoto', data)

    async def send_document(self, chat_id, document, reply_to_message_id=None):
        data = {'chat_id': chat_id, 'document': document}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendDocument', data)

    async def send_video(self, chat_id, video, reply_to_message_id=None):
        data = {'chat_id': chat_id, 'video': video}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendVideo', data)

    async def send_voice(self, chat_id, voice, reply_to_message_id=None):
        data = {'chat_id': chat_id, 'voice': voice}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        return await self._send_request('sendVoice', data)

    def on_message(self, command):
        def decorator(func):
            self._message_handlers[command] = func
            @wraps(func)
            async def wrapper(update):
                await func(update)
            return wrapper
        return decorator

    async def _handle_update(self, update):
        if 'message' in update:
            message = TelegramMessage(update['message'], self)
            if message.data.get('text'):
                text = message.data['text']
                command = text.split()[0]
                if command in self._message_handlers:
                    await self._message_handlers[command](message)

    async def start(self):
        if not self.validate_token():
            self.logger.error("Bot token is invalid. Exiting...")
            return

        self.logger.info("Bot started.")
        offset = None
        while True:
            updates = await self.get_updates(offset)
            if updates:
                for update in updates:
                    await self._handle_update(update)
                    offset = update['update_id'] + 1

    async def get_updates(self, offset=None):
        params = {'timeout': 100, 'offset': offset}
        try:
            response = self.session.get(f"{self.base_url}/getUpdates", params=params)
            if response.status_code == 200:
                updates = response.json()['result']
                return updates
            else:
                self.logger.error(f"Failed to get updates. Status code: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Exception occurred while getting updates: {e}")
            return None
