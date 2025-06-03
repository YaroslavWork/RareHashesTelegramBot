import telegram
from dotenv import load_dotenv
from datetime import datetime
import os
import asyncio
import aio_pika
import time

from command_operation import ping, add_user, remove_user, notify_users, change_rule
from notification import log


async def handle_data(message, channel):    
    '''
    Five types of data:
    |PING| - check connection. params: [ping_id]
    |ADD| - add new user. params: [telegram_id, user_instruction]
    |NEW| - hash has been added. parans: [word, start_from_beginning, hash_type, counts, user, created_at, top]
    |REM| - remove user. params: [telegram_id, user_instruction]
    |CHN| - change user rule. params: [telegram_id, user_instruction]
    
    All parameters separated by: |NEXT|.
    '''
    global BOT

    uuid = message.split('|')[0]
    message = f"|{'|'.join(message.split('|')[1:])}"
    
    if message.startswith("|PING|"):
        data = message.split("|PING|")[1].split("|NEXT|")
        response = ping(data)
    elif message.startswith("|ADD|"):
        data = message.split("|ADD|")[1].split("|NEXT|")
        response = add_user(data, BOT)
    elif message.startswith("|NEW|"):
        data = message.split("|NEW|")[1].split("|NEXT|")
        response = notify_users(data, BOT)
    elif message.startswith("|REM|"):
        data = message.split("|REM|")[1].split("|NEXT|")
        response = remove_user(data, BOT)
    elif message.startswith("|CHN|"):
        data = message.split("|CHN|")[1].split("|NEXT|")
        response = change_rule(data, BOT)
    
    await send(f"{uuid}{response}", channel)

    
async def send(message, channel):
    msg = aio_pika.Message(body=message.encode())
    await channel.default_exchange.publish(msg, routing_key="telegram_to_website")
    log("RabbitMQ", f"Send: {message}")


async def handle_incoming(channel):
    queue = await channel.declare_queue("website_to_telegram", durable=True)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                message = message.body.decode()
                log("RabbitMQ", f"Receive: {message}")
                await handle_data(message, channel)


async def main():
    print("Telegram server is starting...")
    RABBIT_LOGIN = os.getenv('RABBIT_LOGIN').strip()
    RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD').strip()
    RABBIT_HOST = os.getenv('RABBIT_HOST').strip()

    while True:
        log("RabbitMQ", "Connection...")
        try:
            connection = await aio_pika.connect_robust(f"amqp://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{RABBIT_HOST}/")
            channel = await connection.channel()
            log("RabbitMQ", "Connected")
            break
            
        except:
            log("RabbitMQ", "Connection failed...")
            time.sleep(15)

    await asyncio.gather(
        handle_incoming(channel)
    )


if __name__ == "__main__":
    load_dotenv()

    TOKEN = os.getenv('TOKEN')
    BOT = telegram.Bot(token=TOKEN)

    asyncio.run(main())