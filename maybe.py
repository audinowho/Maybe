import discord
import sqlite3
from pokedb import PokeSQL
import os

# Housekeeping for login information
TOKEN_FILE_PATH = 'token.txt'

# The Discord client.
client = discord.Client()

# Command prefix.
COMMAND_PREFIX = '!'

scdir = os.path.dirname(os.path.abspath(__file__))

conn = sqlite3.connect(os.path.join(scdir, 'pokedex.sqlite'))
c = conn.cursor()
db = PokeSQL(c)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message: discord.Message):
    content = message.content

    if not content.startswith(COMMAND_PREFIX):
        return
    args = content[len(COMMAND_PREFIX):].split(' ')

    display_limit = 100
    if args[0] == 'learnset':
        name = args[1].replace('_', ' ')

        lv = 100
        if len(args) > 2:
            lv = int(args[2])

        p_id = db.moveNum(name)
        if p_id == -1:
            await client.send_message(message.channel, content="Cannot find `{}`").format(name)
            return
        
        res = db.learnSet(p_id, lv)
        post = "```Pokémon that can learn #{:03d} {} by level {}:\n".format(p_id, name, lv)
        for ii in range(min(display_limit,len(res))):
            lvs = ["{:02d}".format(x) for x in res[ii][2]]
            post += "\n#{:03d}\t{:<14}\tLv.{}".format(res[ii][0], res[ii][1], "/".join(lvs))
        if len(res) > display_limit:
            post += "\nAnd {} more.".format(len(res) - display_limit)
        post += "```"
        await client.send_message(message.channel, content=post)
    elif args[0] == 'movepool':
        name = args[1].replace('_', ' ')

        lv = 100
        if len(args) > 2:
            lv = int(args[2])

        p_id = db.dexNum(name)
        if p_id == -1:
            await client.send_message(message.channel, content="Cannot find `{}`").format(name)
            return
        
        res = db.movePool(p_id, lv)
        post = "```#{:03d} {}'s level-up moves (up to Lv.{}):\n".format(p_id, name, lv)
        for ii in range(min(display_limit,len(res))):
            post += "\n#{:03d}\t{:<14}\tLv.{:02d}".format(res[ii][0], res[ii][1], res[ii][2])
        if len(res) > display_limit:
            post += "\nAnd {} more.".format(len(res) - display_limit)
        post += "```"
        await client.send_message(message.channel, content=post)
    elif args[0] == 'abilityset':
        name = args[1].replace('_', ' ')
        
        p_id = db.abilityNum(name)
        if p_id == -1:
            await client.send_message(message.channel, content="Cannot find `{}`").format(name)
            return
        
        res = db.abilitySet(p_id)
        post = "```Pokémon with the ability #{:03d} {}:".format(p_id, name)
        for ii in range(min(display_limit,len(res))):
            post += "\n#{:03d}\t{:<14}".format(res[ii][0], res[ii][1])
            if res[ii][2]:
                post += " [HA]"
        if len(res) > display_limit:
            post += "\nAnd {} more.".format(len(res) - display_limit)
        post += "```"
        await client.send_message(message.channel, content=post)
    elif args[0] == 'abilitypool':
        name = args[1].replace('_', ' ')
        
        p_id = db.dexNum(name)
        if p_id == -1:
            await client.send_message(message.channel, content="Cannot find `{}`").format(name)
            return
        
        res = db.abilityPool(p_id)
        post = "```#{:03d} {}'s abilities:".format(p_id, name)
        for ii in range(min(display_limit,len(res))):
            post += "\n#{:03d}\t{:<14}".format(res[ii][0], res[ii][1])
            if res[ii][2]:
                post += " [HA]"
        if len(res) > display_limit:
            post += "\nAnd {} more.".format(len(res) - display_limit)
        post += "```"
        await client.send_message(message.channel, content=post)
    elif args[0] == 'typeset':
        name = args[1].replace('_', ' ')
        
        p_id = db.typeNum(name)
        if p_id == -1:
            await client.send_message(message.channel, content="Cannot find `{}`").format(name)
            return
        
        res = db.typeSet(p_id)
        post = "```Pokémon of the {}-type:".format(name)
        for ii in range(min(display_limit,len(res))):
            post += "\n#{:03d}\t{:<14}".format(res[ii][0], res[ii][1])
        if len(res) > display_limit:
            post += "\nAnd {} more.".format(len(res) - display_limit)
        post += "```"
        await client.send_message(message.channel, content=post)

with open(os.path.join(scdir, TOKEN_FILE_PATH)) as token_file:
    token = token_file.readline().strip()

client.run(token)
