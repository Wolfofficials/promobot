from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import SendMessageRequest
from telethon.errors import PeerFloodError, UserIsBlockedError, ChatWriteForbiddenError, ChatAdminRequiredError
import time
import random

from creds import session, api_id, api_hash

# Create a client instance using the string session
client = TelegramClient(StringSession(session), int(api_id), api_hash)

# Start the client
client.start()


def get_random_message():
    with open('texts.txt', 'r') as file:
        lines = file.readlines()
        return random.choice(lines).strip()


async def broadcast_message():
    groups = await client.get_dialogs()
    groups = [g for g in groups if g.is_group]

    for group in groups:
        try:
            message = get_random_message()
            await client(SendMessageRequest(group, message))
            delay = random.randint(15, 63)
            time.sleep(delay)

        except PeerFloodError:
            time.sleep(50)
            pass
        except UserIsBlockedError:
            pass
        except ChatWriteForbiddenError:
            pass
        except ChatAdminRequiredError:
            pass
        except Exception:
            pass

    print("Message broadcast completed.")


async def main():
    await client.start()

    while True:
        await broadcast_message()
        # Wait for 8 hours before repeating the process
        time.sleep(28800)


with client:
    client.loop.run_until_complete(main())

