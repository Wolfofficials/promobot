import asyncio
import random
import logging
from telethon import TelegramClient, events, sync
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl import functions, types
import time

delay = random.randint(60*60, 60*180)
# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration from a file or environment variables
from creds import session, api_id, api_hash  # Import credentials from creds.py

# Create a client instance using the string session
client = TelegramClient(StringSession(session), api_id, api_hash)

# Start the client
client.start()

# Create a list of groups from the groups.txt file
with open('groups.txt', 'r') as f:
    groups = [line.strip() for line in f if line.strip()]

# Define a function to get the list of chat IDs your client is already a member of
async def get_joined_chats():
    chats = []
    async for dialog in client.iter_dialogs():
        chats.append(dialog.id)
    return chats

# Get the list of all chat IDs (execute this once to save in 'joinedids.txt' if needed)
async def get_all_chat_ids():
    all_chats = await get_joined_chats()
    with open('joinedids.txt', 'w') as f:
        for chat_id in all_chats:
            f.write(str(chat_id) + '\n')

# Define join_group function
async def join_group(group):
    try:
        # Check if the group ID (as a string) is in the list of joined chats
        with open('joinedids.txt', 'r') as f:
            joined_chats = [line.strip() for line in f]
        
        if str(group) in joined_chats:
            logger.info(f'Already a member of chat ID: {group}. Skipping...')
            return
        
        await client(JoinChannelRequest(group))
        logger.info(f'Joined chat ID: {group}')
        time.sleep(delay)  # Removed extra indentation here
    except FloodWaitError as e:
        logger.warning(f'Joining {group} failed due to flooding. Waiting for {e.seconds+(delay)} seconds...')
        await asyncio.sleep(e.seconds)
        await join_group(group)
    except SessionPasswordNeededError:
        logger.error(f'Two-factor authentication is enabled for {group}. Please enter the password.')
        password = input("Enter the two-factor authentication password: ")
        await client(JoinChannelRequest(group, password=password))
        logger.info(f'Joined chat ID: {group}')
    except Exception as e:
        logger.error(f'Error joining chat ID: {group}. Details: {e}')

# Define main coroutine
async def main():
    # Execute get_all_chat_ids() once to save chat IDs in 'joinedids.txt'
    await get_all_chat_ids()

    for group in groups:
        await join_group(group)

# Run the main loop until interrupted
with client:
    client.loop.run_until_complete(main())
