import asyncio
import random
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import SendMessageRequest

# Initialize logging with a StreamHandler
import sys
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(stream=sys.stdout)])
logger = logging.getLogger(__name__)
delay = random.randint(60 * 30, 60 * 180)

from creds import session, api_id, api_hash  # Import credentials from creds.py

# Check if the script is being run independently
if __name__ == "__main__":
    # Create a client instance using the string session
    client = TelegramClient(StringSession(session), api_id, api_hash)

    # Start the client
    async def start_client():
        await client.start()
        print('Successfully logged in.')

    # Specify the chat ID where you want to send logs
    username = 'wolfofficials'

    with open('groups.txt', 'r') as f:
        groups_to_join = [line.strip() for line in f if line.strip()]
        random.shuffle(groups_to_join)

    # Define join_group function
    async def join_group(group):
        try:
            # Attempt to join the group
            await client(JoinChannelRequest(group))
            log_and_send(logging.INFO, f'Joined chat ID: {group}')
            await asyncio.sleep(delay)
        except FloodWaitError as e:
            log_and_send(logging.WARNING, f'Joining {group} failed due to flooding. Waiting for {e.seconds + delay} seconds...')
            await asyncio.sleep(e.seconds + delay)
        except Exception as e:
            log_and_send(logging.ERROR, f'Error joining chat ID: {group}. Details: {e}')
            await asyncio.sleep(delay)
        finally:
            # Remove the group username from groups.txt immediately
            groups_to_join.remove(group)
            with open('groups.txt', 'w') as f:
                for g in groups_to_join:
                    f.write(f'{g}\n')

    # Define send_log_message function
    async def send_log_message(message):
        await client(SendMessageRequest(username, message))

    def log_and_send(level, message):
        logger.log(level, message)
        asyncio.ensure_future(send_log_message(message))

    # Define main coroutine
    async def main():
        while groups_to_join:
            group = groups_to_join[0]  # Get the first group in the list
            await join_group(group)

    # Run the main loop until interrupted
    with client:
        client.loop.run_until_complete(main())
