import os
from typing import Mapping, Optional, List, Any

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Cog, Command, Group

# import interactions
# from interactions import CommandContext, OptionType, Option, OptionChoice, ApplicationCommandType
from datetime import datetime, timezone, timedelta

from utils.config import TOKEN, PGUILD, BGUILD, JOIN_CHANNEL, BOT_DEV_ROLE, DAD_JOKES_API_KEY, LOGGING_LEVEL, \
    LOG_CHANNEL

import requests
import json
import logging


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_group_help()

    async def send_command_help(self, command):
        return await super().send_command_help()


logger = logging.getLogger('discord')
logging.getLogger('discord.http').setLevel(LOGGING_LEVEL)
handler = logging.FileHandler(
    filename='backup/bytehackzbot2.log',
    encoding='utf-8',
    mode='w')
dt_fmt = '%Y-%m-%d %H:%M:%S'
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Define intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False
intents.guilds = True

activity = discord.Activity(type=discord.ActivityType.watching, name="Byte®Hackz")
bot = commands.Bot(command_prefix='!',
                   intents=intents,
                   activity=activity,
                   status=discord.Status.idle,
                   help_command=CustomHelpCommand())


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")
    print(f"Servers: {len(bot.guilds)}")
    print(f"I am in: {[i.name for i in bot.guilds]}")
    print("Bot is online.")


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
async def hello(ctx):
    await ctx.send("Hello, welcome to Byte®Hackz 2023!", emphemeral=True)


@bot.command()
async def goodbye(ctx):
    await ctx.send("Goodbye, have a nice day!")


@bot.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # ignore if it is message sent by the bot
    if 'drink' in message.content or 'water' in message.content:
        embed = discord.Embed(
            title="Remember to stay hydrated.",
            description="Drinking enough water each day is crucial for many reasons: "
                        "\n- to regulate body temperature"
                        "\n- keep joints lubricated"
                        "\n- prevent infections"
                        "\n- deliver nutrients to cells"
                        "\n- keep organs functioning properly"
                        "\n- improves sleep quality, cognition, and mood",
            color=discord.Color.orange()
        )
        embed.set_author(name=message.author,
                         url="https://www.instagram.com/npoverflow/",
                         icon_url=message.author.avatar)
        # embed.set_thumbnail(url="attachment://images/Stay_hydrated.jpg")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1169297244500009022/1169297512650248282/images.png?ex=6554e42b&is=65426f2b&hm=bae43ae3bc83d5e8dae7e3239a874c10804f3a521fdaf52eb91aded7b0ddd770&")
        embed.set_footer(text="Overflow Byte®Hackz 2023 Organising Team",
                         icon_url='https://cdn.discordapp.com/attachments/1169297244500009022/1169837618658291732/logo_white_bg.png?ex=6556db2e&is=6544662e&hm=39691fd6451a1abbdb6a22826c07cb19d6f882aaf6da67abf75d24d9ed565737&')
        await message.channel.send(embed=embed)


@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user:
        return  # ignore if it is message sent by the bot
    else:
        channel = bot.get_channel(int(LOG_CHANNEL))
        embed = discord.Embed(title="Message edited.",
                              description=f"Before: {before.content}\n"
                                          f"After: {after.content}",
                              color=discord.Color.blue())
        embed.set_author(name=before.author,
                         url=before.jump_url,
                         icon_url=before.author.avatar)
        embed.set_footer(text=f"{before.author.id}")
        embed.timestamp = datetime.now(timezone(timedelta(hours=+8), 'MPST'))
        await channel.send(embed=embed)


@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return  # ignore if it is message sent by the bot
    else:
        channel = bot.get_channel(int(LOG_CHANNEL))
        embed = discord.Embed(title=f"Message deleted in <#{message.channel.id}>",
                              description=f"{message.content}",
                              color=discord.Color.red())
        embed.set_author(name=message.author,
                         icon_url=message.author.avatar)
        embed.set_footer(text=f"{message.author.id}")
        embed.timestamp = datetime.now(timezone(timedelta(hours=+8), 'MPST'))
        await channel.send(embed=embed)


@bot.event
async def on_member_update(before, after):
    channel = bot.get_channel(int(LOG_CHANNEL))
    entry = list(await after.guild.audit_logs(limit=1))[0]
    user = entry.user
    if before.display_name != after.display_name:
        embed = discord.Embed(title="Name updated.",
                              description=f"Before: {before.display_name}\n"
                                          f"After: {after.display_name}",
                              color=discord.Color.magenta())
        embed.set_author(name=before.User,
                         icon_url=before.User.avatar)
        embed.set_footer(text=f"{user}({user.id})")
        embed.timestamp = datetime.now(timezone(timedelta(hours=+8), 'MPST'))
        await channel.send(f'{before.mention} changed names.')


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(JOIN_CHANNEL))
    await channel.send("Bye, {member}")


bot.run(TOKEN)
