import asyncio
import time
import re
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sessions import StringSession

# Load configuration from a file or environment variables
from creds import session, api_id, api_hash, owner  # Import credentials from creds.py
delay = (5)
# Create a client instance using the string session
client = TelegramClient(StringSession(session), api_id, api_hash)

# Define the function to get joined groups
async def get_joined_groups():
    dialogs = await client.get_dialogs()
    group_list = []
    for dialog in dialogs:
        if getattr(dialog.entity, 'username', None) and dialog.is_group:
            group_list.append(dialog.entity.username)
        elif dialog.is_group:
            # Handle private groups differently
            group_list.append(f"[Private Group - ID: {dialog.entity.id}]")
    return group_list

# Define the event handler for the ".joined" command
@client.on(events.NewMessage(pattern=r'^\.joined$', from_users=[owner]))
async def joined_command_handler(event):
    joined_groups = await get_joined_groups()
    response = 'Joined groups:\n' + '\n'.join(joined_groups)
    await event.respond(response)

# Define the event handler for the ".getlinks" command
@client.on(events.NewMessage(pattern=r'^\.getlinks\s(.+)', from_users=[owner]))
async def get_links_command_handler(event):
    channel_username = event.pattern_match.group(1)
    
    try:
        # Fetch messages from the channel/group
        messages = await client.get_messages(channel_username, limit=None)
        
        # Extract links from messages
        links = set()
        for message in messages:
            text = message.text or ''
            extracted_links = re.findall(r'https?://\S+', text)
            links.update(extracted_links)
        
        # Split links into chunks of 100
        chunk_size = 100
        link_chunks = [list(links)[i:i + chunk_size] for i in range(0, len(links), chunk_size)]

        # Send link chunks to the owner
        for link_chunk in link_chunks:
            response = '\n'.join(link_chunk)
            await event.respond(response)
            time.sleep(delay)

    except Exception as e:
        await event.respond(f"Error: {e}")

client.start()
client.run_until_disconnected()
