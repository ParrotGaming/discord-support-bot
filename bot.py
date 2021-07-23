from html_handler import *
import os
import shutil
import discord
from discord.ext import commands
from discord import File
from dotenv import load_dotenv
import string
import random
load_dotenv()

base_file = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><link rel=\"stylesheet\" href=\"styles.css\"><title>Saved Transcript</title></head><body>"

token = os.getenv("DISCORD_TOKEN")

prefix = "-"

client = commands.Bot(command_prefix = prefix)

def prep_ticket(dir_name, filename):
    try:
        os.makedirs(dir_name)
        shutil.copy(filename + '.html', '{}/index.html'.format(dir_name))
        shutil.copy('styles.css', '{}/styles.css'.format(dir_name))
        shutil.make_archive(dir_name, 'zip', dir_name)
        os.remove(filename + '.html')
        shutil.rmtree(dir_name + "/")
    except OSError:
        print("Ticket Prep Failed")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("-ticket"))
    print('Logged on as', client.user)

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith(prefix + "close"):
            if os.path.exists(message.channel.name + ".html") == False:
                await message.channel.send("You do not have permission to execute this command")
                return None
            generate_html(message.channel.name + ".html")
            prep_ticket(message.channel.name, message.channel.name)
            await discord.utils.get(message.guild.channels, name=message.channel.name).delete()
            await message.author.send('***Log for {}***'.format(message.channel.name), file=File(message.channel.name + ".zip"))
            os.remove(message.channel.name + ".zip")
            print("file generated")
        elif message.content.startswith(prefix + "ticket"):
            overwrites = {
                message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                message.guild.me: discord.PermissionOverwrite(read_messages=True),
                message.author: discord.PermissionOverwrite(read_messages=True)
            }

            cid = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
            cid = "ticket-" + cid
            await message.guild.create_text_channel(cid, overwrites=overwrites)
            with open(str(cid + ".html"), "a") as output_file:
                output_file.write(base_file)
            print("recording started")
        elif message.channel.name == "support":
            await message.delete()
        else:
            filename = message.channel.name + ".html"
            append_div(message.author.avatar_url, message.author, message.content, filename)

client.run(token)