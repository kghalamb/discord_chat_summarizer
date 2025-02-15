import discord
from keybert import KeyBERT
from transformers import pipeline
from nltk.sentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

load_dotenv()


kw_model = KeyBERT()
sentiment_analyzer = SentimentIntensityAnalyzer()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
TOKEN = os.getenv('TOKEN')

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

    content = ""
    if message.content.startswith("!summarize"):
        try:
            num_messages = int(message.content.split()[1]) if len(message.content.split()) > 1 else 5
            messages = []
            async for msg in message.channel.history(limit=num_messages):
                if msg.author != client.user and not msg.content.startswith("!") and not msg.content.startswith("http"):
                    sentiment = analyze_sentiment(msg.content)
                    messages.insert(0,msg.author.name + "(" + sentiment +  "): " + msg.content)  # Append each message to the list
                    content += msg.content + " "
                else: num_messages += 1
            #print(messages)

            combined_content = ' '.join(content)

            topics = extract_topics(combined_content)
            topic_summary = ", ".join(topics) if topics else "general discussion"
            await message.channel.send(f"Topics: {topic_summary}")
            summary = summarize_text(messages)
            await message.channel.send(f"Summary: {summary}")
        
        except Exception as e:
            await message.channel.send(f"Error Procesing Request: {e}")

    elif message.content.startswith("!help"):
        await message.channel.send("Usage: `!summarize` to summarize the last X messages in the channel.")
    
    elif message.content.startswith("!ping"):
        await message.channel.send("Pong!")

def analyze_sentiment(text):
    """Returns the sentiment score and label for a given message."""
    score = sentiment_analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

def extract_topics(messages):
    """Returns the top 3 topics from the given messages."""
    topics = kw_model.extract_keywords(messages, keyphrase_ngram_range=(1, 1), stop_words='english', use_maxsum=True, nr_candidates=20, top_n=3)
    return [kw[0] for kw in topics]

def summarize_text(messages):
    for row in messages:
        print(row)
    combined_content = ' '.join(messages)
    prompt = combined_content
    summary = summarizer(prompt, max_length=150, min_length=5, do_sample=False)
    return summary[0]['summary_text']

client.run(TOKEN)

