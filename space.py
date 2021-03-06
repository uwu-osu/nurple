import glob
import os
import json

import asyncpg
from discord.ext import commands


async def get_prefix(bot, message):
    conn = await asyncpg.connect(user='space', password='hellowo', database='space', host='127.0.0.1')
    values = await conn.fetch('''SELECT * FROM prefix WHERE guild_id = $1''', message.guild.id)
    await conn.close()
    if len(values) == 0:
        return '-'
    return values[0]['prefix']


client = commands.Bot(command_prefix=get_prefix)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')
    await client.process_commands(message)


with open("config.json") as a:
    config = json.load(a)


# config is now a dictionary object
token = config['token']
for file in glob.glob("commands/*.py"):
    client.load_extension(file.replace(os.sep, ".")[:-3])
client.load_extension("jishaku")
client.run(token)
