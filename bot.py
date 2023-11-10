import os
from typing import Mapping, Optional, List, Any

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Cog, Command, Group

# import interactions
# from interactions import CommandContext, OptionType, Option, OptionChoice, ApplicationCommandType
from datetime import datetime, timezone, timedelta

from utils.config import (TOKEN, PGUILD, BGUILD, JOIN_CHANNEL, BOT_DEV_ROLE,
                          DAD_JOKES_API_KEY, LOGGING_LEVEL, LOG_CHANNEL, OVERFLOW_LOGO,
                          BYTEHACKZ_BANNER, BYTEHACKZ_SQUARE)

import requests
import json
import logging


class aclient(discord.Client):
    def __init__(self):
        # Define intents
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.typing = True
        intents.presences = False
        intents.guilds = True
        activity = discord.Activity(type=discord.ActivityType.watching, name="Byte®Hackz")
        super().__init__(intents=intents, activity=activity)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"Logged in as: {self.user}")
        print(f"Servers: {len(self.guilds)}")
        print(f"I am in: {[i.name for i in self.guilds]}")
        print("Bot is online.")


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
# intents = discord.Intents.default()
# intents.members = True
# intents.message_content = True
# intents.typing = True
# intents.presences = False
# intents.guilds = True

# activity = discord.Activity(type=discord.ActivityType.watching, name="Byte®Hackz")
# client = discord.Client(intents=intents,
#                         activity=activity,
#                         status=discord.Status.idle,
#                         help_command=CustomHelpCommand())
client = aclient()
tree = discord.app_commands.CommandTree(client)


@client.event
# async def on_ready():
#     await tree.sync()
#     print(f"Logged in as: {client.user}")
#     print(f"Servers: {len(client.guilds)}")
#     print(f"I am in: {[i.name for i in client.guilds]}")
#     print("Bot is online.")


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')


@tree.command(name="hello", description="Say hi :)")
async def hello(interaction: discord.Interaction, member:discord.Member):
    await interaction.response.send_message(f"Hello {member.mention}, welcome to Byte®Hackz 2023!")


@tree.command(name="goodbye", description="Say bye :)")
async def goodbye(interaction: discord.Interaction, member:discord.Member):
    await interaction.response.send_message(f"Goodbye {member.mention}, have a nice day!")


@tree.command(description="Sends the bot's latency.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency is {client.latency}ms", ephemeral=True)


@client.event
async def on_message(message):
    if message.author == client.user:
        return  # ignore if it is message sent by the bot

    elif 'drink' in message.content or 'water' in message.content:
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

    elif 'butt' in message.content or 'ass' in message.content:
        embed = discord.Embed(title=":3",
                              description=":smirk:",
                              color=discord.Color.gold())
        embed.set_author(name=message.author,
                         icon_url=message.author.avatar)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1169297244500009022/1169957171107205170/corgi.gif?ex=65574a86&is=6544d586&hm=1eb086ae2a153fd46661082c5517c8899202347b961d4cfed8bdfb0e9756a361&")
        embed.set_footer(text=f"{message.author.id}")
        embed.timestamp = datetime.now(timezone(timedelta(hours=+8), 'MPST'))
        await message.channel.send(embed=embed)

    elif 'hi' in message.content or 'hello' in message.content or 'welcome' in message.content:
        embed = discord.Embed(title="Hello!",
                              description="Welcome to Byte®Hackz 2023!",
                              color=discord.Color.orange())
        embed.set_author(name=message.author,
                         url="https://www.instagram.com/npoverflow/",
                         icon_url=message.author.avatar)
        embed.set_footer(text=f"{message.author.id}",
                         icon_url="https://cdn.discordapp.com/attachments/1169297244500009022/1171721561368186880/bytehackz2023logo_square.jpg?ex=655db5bd&is=654b40bd&hm=f003a0cfe4d7d905f580d8b37a31181fdf5cc1d44f5b114395c7ab6bb62ae108&")
        await message.channel.send(embed=embed)



@tree.command()
async def joke(interaction: discord.Interaction):
    jokeurl = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
        "X-RapidAPI-Key": DAD_JOKES_API_KEY,
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.request("GET", jokeurl, headers=headers)

    if response.status_code == 200:
        joke_data = response.json()
        setup = joke_data.get('setup', '')
        punchline = joke_data.get('punchline', '')

        # Debugging: Print the contents of the joke_data dictionary
        print("joke_data:", joke_data)

        if setup and punchline:
            await interaction.response.send_message(f"Here's a joke:\n{setup}\n{punchline}")
        else:
            await interaction.response.send_message("The joke data is incomplete.")
    else:
        await interaction.response.send_message("Sorry, I couldn't fetch a joke this time.")


@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return  # ignore if it is message sent by the bot
    else:
        channel = client.get_channel(int(LOG_CHANNEL))
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


@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return  # ignore if it is message sent by the bot
    else:
        channel = client.get_channel(int(LOG_CHANNEL))
        embed = discord.Embed(title=f"Message deleted in <#{message.channel.id}>",
                              description=f"{message.content}",
                              color=discord.Color.red())
        embed.set_author(name=message.author,
                         icon_url=message.author.avatar)
        embed.set_footer(text=f"{message.author.id}")
        embed.timestamp = datetime.now(timezone(timedelta(hours=+8), 'MPST'))
        await channel.send(embed=embed)


@client.event
async def on_member_update(before, after, member: discord.Member):
    channel = client.get_channel(int(LOG_CHANNEL))
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
        await channel.send(embed=embed)


@client.event
async def on_member_remove(member:discord.Member):
    channel = client.get_channel(int(JOIN_CHANNEL))
    await channel.send(f"Bye, {member.name}")


client.run(TOKEN)
