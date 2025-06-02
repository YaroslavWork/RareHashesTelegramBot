import asyncio
import telegram

from database_operation import add_user as _add_user, delete_user, get_all_users_data
from telegram_utils import send_message
from notification import log

def ping(messages: list[str]) -> str:
    """
    Ping function ex. |PING|123123

    Args:
        messages (list[str]):
            - PING_ID: str

    Returns:
        Starts with |PING|:
            <int> - ping id in case of success
            errno:
                1 - if length for ping message does not right.
        Example: |PING|123123
    """

    if len(messages) == 1: # [PING ID]
        return f'|PING|{messages[0]}'
    
    log("Command Operation (ping)", "This message is not the correct length.")
    return '|PING|errno|NEXT|1'


def add_user(messages: list[str], bot: telegram.Bot | None = None, default_name = 'users_data') -> str:
    """
    Add user id and rule to text file ex. |ADD|123123|NEXT|M32

    Rule types:
    M means - minimum hash value to sent to user ex. M32 - is minimum 32 zeros or ones to notify a user;
    T means - top for ex. T100 mean hash must be in top 100 to notify user.

    Args:
        messages (list[str]):
            - TELEGRAM_ID - Telegram user id;
            - USER_INSTRUCTION - Rule set by user.
        bot (telegram.Bot, optional): The Telegram bot instance used to send the message.
        default_name (str, optional): Name by default where is save users data. Defaults to 'users_data'.

    Returns:
        Starts with |ADD|:
            suc - if the user is added correctlyю
            errno:
                1 - if length for ping message does not right;
                2 - if something wrong in message;
                3 - if user exists in text file.
        Example: |ADD|suc or |ADD|errno|NEXT|2
    """

    if len(messages) == 2:
        try:
            user_id = messages[0]
            user_instruction_type = messages[1][0]
            user_minimum_value = int(messages[1][1:])

            result = _add_user(user_id, f"{user_instruction_type}{user_minimum_value}", default_name)

            if result == -1:
                log("Command Operation (add_user)", f"User {user_id} is already in the text file.")
                return '|ADD|errno|NEXT|3'

            if bot:
                welcome_message = "Welcome to Rarest Hashes Community! "
                if messages[1][0] == 'M':
                    welcome_message += f"You will receive notifications based on rarity with {messages[1][1:]} zeros or ones."
                else:
                    welcome_message += f"You will receive notifications based on ranking, starting with the TOP {messages[1][1:]}."
                asyncio.create_task(send_message(bot, welcome_message, user_id))
            
            return '|ADD|suc'
        except:
            log("Command Operation (add_user)", f"Message: {str(messages)} are not supported.")
            return '|ADD|errno|NEXT|2'
        
    log("Command Operation (add_user)", f"Message: {str(messages)} is not the correct length.")
    return '|ADD|errno|NEXT|1'


def remove_user(messages: list[str], bot: telegram.Bot | None = None, default_name = 'users_data') -> str:
    """
    Remove user id from text file ex. |REM|123123

    Args:
        messages (list[str]):
            - TELEGRAM_ID - Telegram user id.
        bot (telegram.Bot, optional): The Telegram bot instance used to send the message.
        default_name (str, optional): Name by default where is save users data. Defaults to 'users_data'.

    Returns:
        Starts with |REM|:
            suc - if the user is deleted correctly.
            errno:
                1 - if length for ping message does not right;
                2 - if user is not in the text file.
        Example: |REM|suc or |REM|errno|NEXT|2
    """

    if len(messages) == 1:
        user_id = messages[0]
        result = delete_user(user_id, default_name)
        
        if result == -1:
            log("Command Operation (remove_user)", f"User {user_id} not in the text file.")
            return '|REM|errno|NEXT|2'
        if bot:
            asyncio.create_task(send_message(bot, "This bot will no longer send you notifications.", user_id))
        return '|REM|suc'
    
    log("Command Operation (remove_user)", f"Message: {str(messages)} is not the correct length.")
    return '|REM|errno|NEXT|1'


def notify_users(messages: list[str], bot: telegram.Bot, default_name: str = 'users_data') -> str:
    """
    Notify users about a new hash ex. |NEW|foo|NEXT|True|NEXT|sha256|NEXT|27|NEXT|test|NEXT|2025-03-22-12:32:12.124512|NEXT|2310

    Args:
        messages (list[str]): 
            - WORD - Hash word;
            - START_FROM_BEGINNING - check if zeros or ones starts from beginning;
            - HASH_TYPE - ex. sha256;
            - COUNTS - how many zeros or ones in a row;
            - USER - user name;
            - CREATED_AT - data time;
            - TOP - hash ranking.
        bot (telegram.Bot): The Telegram bot instance used to send the message.
        default_name (str, optional): Name by default where is save users data. Defaults to 'users_data'.

    Returns:
        Starts with |NEW|:
            suc - if the user is deleted correctly.
            errno:
                1 - if length for ping message does not right;
                2 - if user is not in the text file.
        Example: |NEW|suc or |NEW|errno|NEXT|2
    """
    
    if len(messages) == 7: # [WORD, START FROM BEGINNING, HASH TYPE, COUNTS, USER, CREATED_AT, TOP]
        prompt = f"TOP {messages[6]}\nWord: {messages[0]}\nCounts: {messages[3]}\nUser: {messages[4]}\nCreated at: {messages[5]}"

        try:
            users_data = get_all_users_data(default_name)
            for user_data in users_data:
                user_data = user_data.split("-") # [USER ID, USER INSTRUCTION]
                user_id = user_data[0]
                user_instruction_type = user_data[1][0]
                user_count = int(user_data[1][1:])
                
                if user_instruction_type == 'M': # Minimum
                    if int(messages[3]) >= user_count:
                        asyncio.create_task(send_message(bot, prompt, user_id))
                else: # Top
                    if int(messages[6]) <= user_count:
                        asyncio.create_task(send_message(bot, prompt, user_id))
            return '|NEW|suc'
        except:
            log("Command Operation (notify_users)", f"Message: {str(messages)} are not supported.")
            return '|NEW|errno|NEXT|2'
    
    log("Command Operation (notify_users)", f"Message: {str(messages)} is not the correct length.")
    return '|NEW|errno|NEXT|1'