import discord
import os
from transformers import pipeline


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
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
        try:
            num_messages = 50#int(message.content.split()[1]) if len(message.content.split()) > 1 else 5
            messages = []
            async for msg in message.channel.history(limit=num_messages):
                if msg.author != client.user:
                    messages.append(msg)  # Append each message to the list
                else: num_messages += 1
            summary = summarize_text(messages)
            await message.channel.send(f"Summary: {summary}")
        except Exception as e:
            await message.channel.send(f"Error Procesing Request: {e}")

    elif message.content.startswith("!help"):
        await message.channel.send("Usage: `!summarize` to summarize the last X messages in the channel.")
    
    elif message.content.startswith("!ping"):
        await message.channel.send("Pong!")



def summarize_text(messages):
    combined_content = ' '.join([msg.content for msg in messages])
    summary = summarizer(combined_content, max_length=100, min_length=5, do_sample=False)
    return summary[0]['summary_text']

client.run(TOKEN)
