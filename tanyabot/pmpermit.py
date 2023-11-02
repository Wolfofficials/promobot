import time
import asyncio
from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession

from creds import session, api_id, api_hash

# Create a client instance using the string session
client = TelegramClient(StringSession(session), int(api_id), api_hash)

# Start the client
client.start()

# Dictionary to keep track of message count per user
message_count_dict = {}


@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    if not event.is_private:
        return  # Ignore messages from groups and channels

    sender_id = event.sender_id

    # Check if the sender is a bot
    sender = await event.get_sender()
    if sender.bot:
        return

    # Check if the sender has sent more than 5 messages in the last minute
    message_count = message_count_dict.get(sender_id, 0)
    current_time = time.time()
    if message_count >= 5 and current_time - message_count_dict[sender_id] <= 60:
        # Stop replying to the user
        return

    # Increment the message count and update the last message time
    message_count_dict[sender_id] = message_count + 1
    message_count_dict[sender_id] = current_time

        # Mark the message as seen
    await event.message.mark_read()

    # Wait for 2 seconds
    time.sleep(2)

    # Simulate typing indicator for 3 seconds
    async with client.action(sender_id, 'typing'):
        await asyncio.sleep(3)

    # Send the message
    await event.respond('Hlo I am Tanya Singh from Delhi.If you want to see my private photos and videos,click on the link below now /n https://t.me/+1BLchlZjMQM5NjMQM5NGNl And enjoy 💋💋')

async def main():
    try:
        await client.start()
        print('Successfully logged in.')
        await client.run_until_disconnected()
    except Exception as e:
        print(f'Error: {str(e)}')

with client:
    client.loop.run_until_complete(main())