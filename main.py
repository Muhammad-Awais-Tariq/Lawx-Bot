import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
import typing
import json
import datetime
import webserver

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
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
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
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
async def kick(ctx, members: commands.Greedy[discord.Member],*, reason: str):
    for member in members:
        try:
            await member.send(f"you have been kicked for following reason:  {reason}")
        except discord.Forbidden:
            await ctx.send("Message not send")
        await member.kick(reason=reason)

@bot.command()
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
async def purge(ctx):
        await ctx.channel.delete()
        new_channel = await ctx.channel.clone(reason="Channel was purged")
        await new_channel.edit(position=ctx.channel.position)
        await new_channel.send("Channel was purged")

@bot.command()
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
async def clear_messages(ctx ,num: int  = 5):
    try:
        deleted = await ctx.channel.purge(limit=num + 1)
        await ctx.send(f'Deleted {len(deleted)} messages.')
    except discord.errors.Forbidden:
        await ctx.send("I don't have the required permissions to delete messages.")

async def timeout_member(ctx, member: discord.Member, minutes: int, *, reason: str = "No reason provided"):
    duration = datetime.timedelta(minutes=minutes)
    
    await member.timeout(duration, reason=reason)
    await ctx.send(f"{member.mention} has been timed out for {minutes} minutes. Reason: {reason}")

@bot.command()
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
async def timeout(ctx, member: discord.Member, minutes: int, *, reason: str = "No reason provided"):
    await timeout_member(ctx, member=member, minutes=minutes, reason=reason)

async def give_warning(member, channel):
    try:
        with open("warning.json", "r") as f:
            data = json.load(f)
    except:
        data = {}

    user_id = str(member.id)

    if user_id not in data:
        data[user_id] = 0

    data[user_id] += 1
    count = data[user_id]

    await channel.send(f"{member.mention} now has {count} warning(s)")

    if count >= 3:
        try:
            await member.timeout(
                datetime.timedelta(minutes=5),
                reason="Reached 3 warnings"
            )

            await channel.send(f"{member.mention} has been timed out for 5 minutes")

            data[user_id] = 0  

        except Exception as e:
            await channel.send("Timeout failed (check permissions / role hierarchy)")

    with open("warning.json", "w") as f:
        json.dump(data, f)

@bot.command()
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
async def untimeout(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"The timeout for {member.mention} has been removed.")

@bot.command()
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
async def warn(ctx, members: commands.Greedy[discord.Member]):
    for member in members:
        await give_warning(member, ctx.channel)

@bot.command()
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
async def assign(ctx, member: discord.Member, role: discord.Role):
    try:
        await member.add_roles(role)
        await ctx.send(f"{member.mention} has been assigned {role.name}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to assign this role.")

@bot.command()
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
async def deafen(ctx, member: discord.Member):
    if not member.voice:
        await ctx.send("User is not in a voice channel.")
        return

    try:
        await member.edit(deafen=True)
        await ctx.send(f"{member.mention} you have been deafened.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to do that.")
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command()
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
async def undeafen(ctx, member: discord.Member):
    if not member.voice:
        await ctx.send("User is not in a voice channel.")
        return

    try:
        await member.edit(deafen=False)
        await ctx.send(f"{member.mention} you have been undeafened.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to do that.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
async def mute(ctx, member: discord.Member):
    if not member.voice:
        await ctx.send("User is not in a voice channel.")
        return

    try:
        await member.edit(mute=True)
        await ctx.send(f"{member.mention} you have been muted.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to do that.")
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command()
@commands.has_any_role("🩸 Crib Mod", "Hoodie")
async def unmute(ctx, member: discord.Member):
    if not member.voice:
        await ctx.send("User is not in a voice channel.")
        return

    try:
        await member.edit(mute=False)
        await ctx.send(f"{member.mention} you have been unmuted.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to do that.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    with open("offensivewords.txt", "r") as f:
        words = [w.strip().lower() for w in f.readlines()]

    message_words = message.content.lower().split()

    for word in words:
        if word in message_words:
            await message.delete()
            await message.author.send(
                f"{message.author.mention} Do not use the word {word}"
            )
            await give_warning(message.author, message.channel)
            break

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send(f"{ctx.author.mention} you do not have permission to use this command.")   

webserver.keep_alive()
bot.run(token,log_handler=handler,log_level=logging.DEBUG)