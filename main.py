import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

import os
import asyncio

load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = os.getenv('SERVER_PORT')
USERS_ID = []
BOT = telegram.Bot(token=TOKEN)


async def wait_for_message(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Client connected: {addr}")

    try:
        while True:
            data = await reader.read(2048)
            if not data:
                break  # Client disconnected

            message = data.decode("utf-8")
            messages = message.split("|NEXT|")

            
            if len(messages) == 6:
                if int(messages[3]) >= 32:
                    prompt = f"Word: {messages[0]}\n\
Start from beggining: {messages[1]}\n\
Hash type: {messages[2]}\n\
Counts: {messages[3]}\n\
User: {messages[4]}\n\
Created at: {messages[5]}"
                await send_message(prompt)
    except Exception as e:
        print(f"Socket error with {addr}: {e}")

    writer.close()
    await writer.wait_closed()
    print(f"Client disconnected: {addr}")
    

async def send_message(message: str):
    global BOT

    for user_id in USERS_ID:
        try:
            await BOT.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

async def run_socket_server():
    server = await asyncio.start_server(wait_for_message, SERVER_HOST, SERVER_PORT)
    addr = server.sockets[0].getsockname()
    print(f"Socket server running on {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    with open('users_id.txt', 'r') as file:
        USERS_ID = file.read().strip().split(';')
        if USERS_ID[-1] == '':
            del USERS_ID[-1]
    
    asyncio.run(run_socket_server())