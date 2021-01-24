import re
import requests

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv




load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_MATH')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    said = message.content.lower()
    if '!differentiate' in said or '!derivative' in said or '!derive' in said:
        #takes question
        text = said
        isCan = False
        if 'can' in text.lower():
            isCan = True
        wkey = 'LA3424-GW7V4VQREX'

        part = re.search('(?:derivative of|derive|differentiate) (.*)',
                         text).groups()[-1]
        #prints equation

        print(part)
        # converts the equation in part so that its safe to put in url
        part = urllib.parse.quote_plus(part)
        url1 = f'http://api.wolframalpha.com/v1/spoken?appid={wkey}&i=what+is+the+derivative+of+{part}%3f'
        url2 = f'http://api.wolframalpha.com/v1/simple?appid={wkey}&i=what+is+the+derivative+of+{part}%3F'
        response = requests.get(url1)
        response = response.text
        response = re.search('(is .*)', response).groups()[-1]
        pic = requests.get(url2, stream=True)
        mimetype = pic.headers['Content-Type']
        raw_bytes = pic.content
        data_url = build_data_url(mimetype, raw_bytes)
        image_html = f'<img src="{data_url}">'
        TEMP = "https://www5b.wolframalpha.com/Calculate/MSP/MSP651140gdii12hh30ggb000056dbie7348eb1g3c?MSPStoreType=image/gif&s=56"
        msg = response
        # message['text'] = message['text'] + response + '.' + f"<br><img style='display:block; width:200px;height:200px;' id='base64image' src='data:image/jpeg;base64', {pic}>"
        if isCan:
            msg = 'Yes I can!\n' + msg

        await message.channel.send(msg)

client.run(TOKEN)