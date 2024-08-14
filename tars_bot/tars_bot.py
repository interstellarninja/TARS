# tars_main.py

import discord
from discord.ext import commands
import logging
from datetime import datetime
import asyncio
from config import load_config
from discord_commands import setup_commands
from github_reader import setup_github
from ai_utils import call_ai, setup_ai

# Set up logging
log_filename = f"tars_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

# Load configuration
config = load_config()

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'TARS is online and ready to explore the cosmos as {bot.user.name} (ID: {bot.user.id})')
    logging.info('------')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message is in a direct message channel
    if isinstance(message.channel, discord.DMChannel):
        # Retrieve the last k messages from the channel for context
        k = 10  # You can adjust this value as needed
        history = [msg async for msg in message.channel.history(limit=k)]  # Use async for without flatten
        context = "\n".join(msg.content for msg in history)  # Include all messages for context

        # Log the previous context for debugging
        logging.info(f"Previous context: {context}")

        # Forward the message and context to OpenAI for a response
        try:
            response = await call_ai(bot, context + "\n" + message.content, max_tokens=1500)
            await message.channel.send(response)
        except Exception as e:
            await message.channel.send(f"Looks like our AI got lost in a wormhole. Error: {str(e)}")
    
    # Process commands
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found in this sector of space. Use !help to see available commands.")
    else:
        await ctx.send(f"A cosmic disturbance occurred: {str(error)}")

async def main():
    # Setup components
    await setup_github(bot, config)
    await setup_ai(bot, config)
    setup_commands(bot)

    # Run the bot
    async with bot:
        await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())