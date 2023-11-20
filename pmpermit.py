import time
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from creds import session, api_id, api_hash

# Check if the script is being run independently
if __name__ == "__main__":
    # Create a client instance using the string session
    client = TelegramClient(StringSession(session), int(api_id), api_hash)

    # Start the client
    async def start_client():
        await client.start()
        print('Successfully logged in.')

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
    
        if message_count >= 10:
            # Stop replying to the user
            return

        # Increment the message count and update the last message time
        message_count_dict[sender_id] = message_count + 1

        # Mark the message as seen
        await event.message.mark_read()

        # Simulate typing indicator for 3 seconds
        async with client.action(sender_id, 'typing'):
            await asyncio.sleep(3)

        # Get your account's first name
        me = await client.get_me()
        my_name = me.first_name

        # Send the message with your name
        response = f'Hello, I am {my_name} from Delhi. If you want to see my private photos and videos, click on the link below now\nhttps://t.me/+1BLchlZjMQM5NGNl and enjoy! 💋💋'
        await event.respond(response)

    async def main():
        try:
            await start_client()
            await client.run_until_disconnected()
        except Exception as e:
            print(f'Error: {str(e)}')

    # Run the main loop if the script is executed directly
    asyncio.run(main())
