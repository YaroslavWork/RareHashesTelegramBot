import telegram


async def send_message(bot: telegram.Bot, message: str, user_id: str) -> bool:
    """
    Sends a text message to a specific Telegram user.

    Args:
        bot (telegram.Bot): The Telegram bot instance used to send the message.
        message (str): The message text to send.
        user_id (str): The ID of the recipient user.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    
    try:
        await bot.send_message(chat_id=user_id, text=message)
        return True
    except Exception as e:
        print(f"Failed to send message to {user_id}: {e}")
        return False