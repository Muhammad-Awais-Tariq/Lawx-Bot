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
        try:
            await member.send(f"you have been banned for following reason: {reason}")
        except discord.Forbidden:
            await ctx.send("Message not send")
        await member.ban(delete_message_seconds=delete_seconds, reason=reason)

@bot.command()
async def kick(ctx, members: commands.Greedy[discord.Member],*, reason: str):
    for member in members:
        try:
            await member.send(f"you have been kicked for following reason:  {reason}")
        except discord.Forbidden:
            await ctx.send("Message not send")
        await member.kick(reason=reason)

@bot.command()
async def purge(ctx):
        await ctx.channel.delete()
        new_channel = await ctx.channel.clone(reason="Channel was purged")
        await new_channel.edit(position=ctx.channel.position)
        await new_channel.send("Channel was purged")

@bot.command(name='wipe')
async def clear_messages(ctx ,num: int  = 5):
    try:
        deleted = await ctx.channel.purge(limit=num + 1)
        await ctx.send(f'Deleted {len(deleted)} messages.')
    except discord.errors.Forbidden:
        await ctx.send("I don't have the required permissions to delete messages.")
bot.run(token,log_handler=handler,log_level=logging.DEBUG)