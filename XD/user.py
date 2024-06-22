class TelegramUserbot:
    """
    Represents a Telegram user or bot.

    Args:
        id (int): Unique identifier for this user or bot.
        is_bot (bool): True if this user is a bot.
        first_name (str): User's or bot's first name.
        last_name (str, optional): User's or bot's last name.
        username (str, optional): User's or bot's username.
        language_code (str, optional): IETF language tag of the user's language.
        can_join_groups (bool, optional): True if the bot can be invited to groups.
        can_read_all_group_messages (bool, optional): True if privacy mode is disabled for the bot.
        supports_inline_queries (bool, optional): True if the bot supports inline queries.
        is_premium (bool, optional): True if this user is a Telegram Premium user.
        added_to_attachment_menu (bool, optional): True if this user added the bot to the attachment menu.
        can_connect_to_business (bool, optional): True if the bot can be connected to a Telegram Business account.

    Attributes:
        id (int): Unique identifier for this user or bot.
        is_bot (bool): True if this user is a bot.
        first_name (str): User's or bot's first name.
        last_name (str, optional): User's or bot's last name.
        username (str): User's or bot's username.
        language_code (str, optional): IETF language tag of the user's language.
        can_join_groups (bool, optional): True if the bot can be invited to groups.
        can_read_all_group_messages (bool, optional): True if privacy mode is disabled for the bot.
        supports_inline_queries (bool, optional): True if the bot supports inline queries.
        is_premium (bool, optional): True if this user is a Telegram Premium user.
        added_to_attachment_menu (bool, optional): True if this user added the bot to the attachment menu.
        can_connect_to_business (bool, optional): True if the bot can be connected to a Telegram Business account.
    """
    

    def __init__(self,
             api_kwargs,
             id,
             first_name,
             is_bot,
             last_name=None,
             username=None,
             language_code=None,
             can_join_groups=None,
             can_read_all_group_messages=None,
             supports_inline_queries=None,
             is_premium=None,
             added_to_attachment_menu=None,
             can_connect_to_business=None):
        super().__init__(api_kwargs=api_kwargs)
        self.id = id
        self.first_name = first_name
        self.is_bot = is_bot
        self.last_name = last_name
        self.username = username
        self.language_code = language_code
        self.can_join_groups = can_join_groups
        self.can_read_all_group_messages = can_read_all_group_messages
        self.supports_inline_queries = supports_inline_queries
        self.is_premium = is_premium
        self.added_to_attachment_menu = added_to_attachment_menu
        self.can_connect_to_business = can_connect_to_business
        self._id_attrs = (self.id,)
        self._freeze()

    def send_message(self, chat_id, text):
        """
        Sends a message to the specified chat ID.
        Args:
            chat_id (int): The target chat ID.
            text (str): The message text.
        """
        url = f"{self.base_url}/sendMessage?chat_id={chat_id}&text={text}"
        self.session.get(url)
        print(f"sending message to chat {chat_id}: {text}")
