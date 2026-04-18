import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
import typing

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename="Discord.log" , encoding="utf-8" , mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("ready")

@bot.command()
async def ban(ctx, members: commands.Greedy[discord.Member],
                   delete_days: typing.Optional[int] = 0, *,
                   reason: str):
    delete_seconds = delete_days * 86400 
    for member in members:
        await member.send(f"you have been banned for following reason {reason}")        
        await member.ban(delete_message_seconds=delete_seconds, reason=reason)


bot.run(token,log_handler=handler,log_level=logging.DEBUG)