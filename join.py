import asyncio
import random
import logging
from telethon import TelegramClient, events, sync
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import JoinChannelRequest
import time

delay = random.randint(60 * 30, 60 * 180)

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

# Define join_group function
async def join_group(group):
    try:
        # Attempt to join the group
        await client(JoinChannelRequest(group))
        logger.info(f'Joined chat ID: {group}')
        asyncio.sleep(delay)
    except FloodWaitError as e:
        logger.warning(f'Joining {group} failed due to flooding. Waiting for {e.seconds + delay} seconds...')
        await asyncio.sleep(e.seconds + delay)
    except Exception as e:
        logger.error(f'Error joining chat ID: {group}. Details: {e}')
    finally:
        # Remove the group username from groups.txt immediately
        groups.remove(group)
        with open('groups.txt', 'w') as f:
            for g in groups:
                f.write(f'{g}\n')

# Define main coroutine
async def main():
    while groups:
        group = groups[0]  # Get the first group in the list
        await join_group(group)

# Run the main loop until interrupted
with client:
    client.loop.run_until_complete(main())
