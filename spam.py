from telethon.sync import TelegramClient
from telethon import functions
from telethon.sessions import StringSession
from telethon.tl.functions.messages import SendMessageRequest
from telethon.errors import PeerFloodError, UserIsBlockedError, ChatWriteForbiddenError, ChatAdminRequiredError
import time
import random
import logging

from creds import session, api_id, api_hash

client = TelegramClient(StringSession(session), int(api_id), api_hash)
client.start()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

owner = 'wolfofficials'  

def get_random_message():
    with open('texts.txt', 'r') as file:
        lines = file.readlines()
        return random.choice(lines).strip()

async def send_message(error_message, group_name):
    formatted_error_message = f"SPM: ({error_message}) in ({group_name})"
    
    try:
        await client(SendMessageRequest(owner, formatted_error_message))
    except Exception as e:
        # Log error if sending the error message fails
        logger.error(f"Error sending formatted error message: {e}")

async def broadcast_message():
    groups = await client.get_dialogs()
    groups = [g for g in groups if g.is_group]

    random.shuffle(groups)

    for group in groups:
        try:
            message = get_random_message()
            await client(SendMessageRequest(group, message))
            delay = random.randint(31, 132)
            time.sleep(delay)

        except PeerFloodError as e:
            await send_message("PeerFloodError", group.name)
            time.sleep(50)
            pass
        except UserIsBlockedError as e:
            await send_message("UserIsBlockedError", group.name)
            pass
        except ChatWriteForbiddenError as e:
            await send_message("ChatWriteForbiddenError", group.name)
            await client(functions.channels.LeaveChannelRequest(group.id))
            await send_message("left group", group.name)
            
            pass
        except ChatAdminRequiredError as e:
            await send_message("ChatAdminRequiredError", group.name)
            pass
        except Exception as e:
            # Log all other errors
            logger.error(f"Error in group {group}: {e}")
            await send_message(f"Error: {e}", group.name)

            print(f"completed")
            await send_message("Broadcast Complete")

async def main():
    await client.start()

    while True:
        await broadcast_message()
        # Wait before repeating the process
        time.sleep(28800)

with client:
    client.loop.run_until_complete(main())
