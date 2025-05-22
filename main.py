import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from datetime import datetime


import os
import asyncio
import aio_pika


def update_users():
    global USERS_ID

    with open('users_id.txt', 'r') as file:
        USERS_ID = [uid for uid in file.read().strip().split(';') if uid]
    return


async def ping(messages: list[str]):
    if len(messages) == 1: # [PING ID]
        return f'|PING|{messages[0]}'
    return f'|PING|errno|NEXT|0'


async def add_user(messages: list[str]):
    global MIN_HASH, USERS_ID

    if len(messages) == 2: # [TELEGRAM ID, USER INSTRUCTION]
        try:
            if f"{messages[0]}-{messages[1]}" in USERS_ID:
                return "|ADD|errno|NEXT|2"
            # M means - minimum hash value to sent to user ex. M32 - is minimum 32 zeros or ones to notify a user
            # T means - top for ex. T100 mean hash must be in top 100 to notify user
            if messages[1][0] in ['T', 'M'] and int(messages[1][1:]) >= MIN_HASH:
                with open('users_id.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{messages[0]}-{messages[1]};')
                update_users()
                return "|ADD|suc"
        except:
            print("This message are not supported")
            return "|ADD|errno|NEXT|1"
    return "|ADD|errno|NEXT|0"


async def notify_users(messages: list[str]):
    global USERS_ID
    
    if len(messages) == 7: # [WORD, START FROM BEGINNING, HASH TYPE, COUNTS, USER, CREATED_AT, TOP]
        prompt = f"TOP {messages[6]}\nWord: {messages[0]}\nCounts: {messages[3]}\nUser: {messages[4]}\nCreated at: {messages[5]}"

        try:
            for user_id in USERS_ID:
                user_data = user_id.split("-") # [USER ID, USER INSTRUCTION]
                user_type = user_data[1][0]
                user_count = int(user_data[1][1:])

                if user_type == 'M': # Minimum
                    if int(messages[3]) >= user_count:
                        await send_message(prompt, user_data[0])
                else: # Top
                    if int(messages[6]) <= user_count:
                        await send_message(prompt, user_data[0])
            return f'|NEW|suc'
        except:
            print("This message are not supported")
            return "|ADD|errno|NEXT|1"
        
    return f'|NEW|errno|NEXT|0'
            

async def handle_data(message, channel):       
    '''
    Three types of data:
    |PING| - check connection. params: [ping_id]
    |ADD| - add new user. params: [telegram_id, user_instruction]
    |NEW| - hash has been added. parans: [word, start_from_beginning, hash_type, counts, user, created_at, top]
    
    All parameters separated by: |NEXT|.
    '''
    if message.startswith("|PING|"):
        data = message.split("|PING|")[1].split("|NEXT|")
        response = await ping(data)
    elif message.startswith("|ADD|"):
        data = message.split("|ADD|")[1].split("|NEXT|")
        response = await add_user(data)
    elif message.startswith("|NEW|"):
        data = message.split("|NEW|")[1].split("|NEXT|")
        response = await notify_users(data)

    await send(response, channel)


async def send_message(message: str, user_id: str):
    global BOT
    try:
        await BOT.send_message(chat_id=user_id, text=message)
        return True
    except Exception as e:
        print(f"Failed to send message to {user_id}: {e}")
        return False
    
async def send(message, channel):
    msg = aio_pika.Message(body=message.encode())
    await channel.default_exchange.publish(msg, routing_key="telegram_to_website")
    now = datetime.now()
    formatted = now.strftime("%d.%m.%Y %H:%M:%S.") + f"{now.microsecond:03d}"
    print(f"({formatted}) Send: {message}")


async def handle_incoming(channel):
    queue = await channel.declare_queue("website_to_telegram", durable=True)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                message = message.body.decode()
                now = datetime.now()
                formatted = now.strftime("%d.%m.%Y %H:%M:%S.") + f"{now.microsecond:03d}"
                print(f"({formatted}) Receive: {message}")
                await handle_data(message, channel)

async def main():
    connection = await aio_pika.connect_robust(f"amqp://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{RABBIT_HOST}/")
    channel = await connection.channel()

    await asyncio.gather(
        handle_incoming(channel)
    )


if __name__ == "__main__":
    load_dotenv()

    MIN_HASH = 25
    TOKEN = os.getenv('TOKEN')
    SERVER_HOST = os.getenv('SERVER_HOST')
    SERVER_PORT = os.getenv('SERVER_PORT')
    RABBIT_LOGIN = os.getenv('RABBIT_LOGIN').strip()
    RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD').strip()
    RABBIT_HOST = os.getenv('RABBIT_HOST').strip()
    USERS_ID = []
    BOT = telegram.Bot(token=TOKEN)

    update_users()

    asyncio.run(main())