import discord
import os


TOKEN = "MTM0MDI0Mjg0MjkwMzM4NDA4Ng.GJi71f.BYMCp7PI9gdxNDrEnSoQOthwsqXlKXTANdPo80"

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Required to read message content

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore own messages

    if message.content.startswith("!summarize"):
        channel = message.channel
        messages = []
        
        async for msg in channel.history(limit=50):  # Adjust limit as needed
            if message.author != client.user:
                messages.append(msg.content)

        print(f"Messages: {messages}")
        full_text = "\n".join(messages)
        summary = summarize_text(full_text)  # Call NLP function (to be implemented)
        
        await channel.send(f"**Summary:**\n{summary}")
    elif message.content.startswith("!help"):
        await message.channel.send("Usage: `!summarize` to summarize the last 50 messages in the channel.")
    elif message.content.startswith("!ping"):
        await message.channel.send("Pong!")

def summarize_text(text):
    return "Summary function not implemented yet!"

client.run(TOKEN)
