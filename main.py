# bot.py
import os
import random

from keep_alive import keep_alive

import discord
from discord.ext import commands
from dotenv import load_dotenv

import re
import requests
import base64
import urllib

keep_alive()

def build_data_url(mimetype, raw_bytes):
  base64_bytes = base64.b64encode(raw_bytes)
  base64_str = base64_bytes.decode('ascii')
  return f"data:{mimetype};base64,{base64_str}"


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        'Could you please use this bot to add your name!!! Use the command:\nsetname <firstname> <lastname>\nin any channel on the server'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    said = message.content.lower()
    if 'hello!' in said and str(message.channel) != 'community-area':
        await message.channel.send('Have you kicked Nathan yet?')
        reason = await client.wait_for('message')
        if 'no' in reason.content:
            await message.channel.send(':frowning:')
        elif 'ye' in reason.content:
            await message.channel.send('YAYY!!!')
    if 'bye!' in said and str(message.channel) != 'community-area':
        await message.channel.send('Kick Nathan!')
    if ('bored' in said and str(message.channel) != 'community-area') or 'bored!' in said:
        await message.channel.send('Why?')
        reason = await client.wait_for('message')
        if 'tired' in reason.content:
            await message.channel.send(':sleeping:')
        else:
            await message.channel.send('Me too!')
    if 'im sad' in said:
        await message.channel.send('Why?')
        reason = await client.wait_for('message')
        if 'idk' in reason.content:
            await message.channel.send(':frowning:\nHow can I help?')
            newreason = await client.wait_for('message')
            await message.channel.send(f'sure! I will {newreason.content}')
        else:
            await message.channel.send("It's alright! :slight_smile:")
    if '^-^' in said and str(message.channel) != 'community-area':
        await message.channel.send('^-^')
    if '!bleh' in said:
        with open('bleh.png', 'rb') as fp:
            await message.channel.send(file=discord.File(fp, 'new_filename.png'))
    if 'seeaaron' in said:
        await message.channel.send('Go Away!')
    if 'seedickson' in said:
        with open('dickson-pic.jpg', 'rb') as fp:
            await message.channel.send(file=discord.File(fp, 'new_filename.png'))
    if 'seemitchell' in said:
        with open('mitchell-pic.png', 'rb') as fp:
            await message.channel.send(file=discord.File(fp, 'new_filename.png'))
    if 'seaaaron' in said:
        await message.channel.send('Go Away!')
    if '!mochi' in said:
        with open('mochi.jpg', 'rb') as fp:
            await message.channel.send(file=discord.File(fp, 'new_filename.png'))
    if 'randquote' == said:
        quoteFile = open('orwellquote.txt')
        counter = 0
        d = {}
        for line in quoteFile:
            counter += 1
            line = line.rstrip()
            d[counter] = line
        quotenum = random.randint(1, counter)
        await message.channel.send(d[quotenum])
    if 'randorwell' in said:
        quoteFile = open('nef.txt')
        counter = 0
        d = {}
        for line in quoteFile:
            counter += 1
            line = line.rstrip()
            d[counter] = line
        quotenum = random.randint(1, counter)
        await message.channel.send(d[quotenum])
    if '!feedback' in said:
        await message.channel.send('Feedback noted!')
    if said == '!heads' or said == '!tails':
        randomGame = random.randint(1,2)
        if randomGame == 1:
          randomGame = '!heads'
        else:
          randomGame = '!tails'
        if randomGame == said:
          await message.channel.send('You win!!!')
        else:
          await message.channel.send('You lost :frowning:')
    if '!differentiate' in said or '!derivative' in said or '!derive' in said:
        #takes question
        text = said
        isCan = False
        if 'can' in text.lower():
          isCan = True
        wkey = 'LA3424-GW7V4VQREX'
        
        part = re.search('(?:derivative of|derive|differentiate) (.*)',text).groups()[-1]
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



    #id crisis
    if 'setname ' in said:
        identityList = open('identityList.txt', 'r')
        namesList = []
        for line in identityList:
          namesList.append(line.split(',')[0])
        identityList.close()
        # new identity
        idList = said.split(' ')
        print(f'MY ID IS <@{message.author.id}>')
        print(namesList)
        if f'<@{message.author.id}>' in namesList or f'<@!{message.author.id}>' in namesList:
            await message.channel.send('Go Away')
        else:
            await message.channel.send(f'<@{message.author.id}> {idList[1].title()}')
            identityList = open('identityList.txt', 'a')
            print(f'{message.author.mention},{idList[1].title()} {idList[2].title()}', file=identityList)
        identityList.close()
        # edit identity message
        identityList = open('identityList.txt', 'r')
        d = {}
        pinglist = []
        content = ''
        print(f'identitylist is {identityList}')
        for line in identityList:
            line = line.rstrip().split(',')
            print(f'line is {line}')
            personName = line[1]
            if personName not in pinglist:
              pinglist.append(personName)
            else:
              personName = personName + '1'
            d[personName] = [line[0], personName]
        identityList.close()
        pinglist.sort()
        print(pinglist)
        channel = client.get_channel(757948169362473050)
        msg = await channel.fetch_message(759706606577123358)
        for person in pinglist:
          content += f'{d[person][0]} {person}\n'
        content = f'{len(pinglist)} people have solved the crisis\n{content}'
        await msg.edit(content=content)
    if 'setcode' in said:
        command, code, server = said.split(' ')
        amongwrite = open('amongcode.txt', 'w')
        print(f'{code},{server}', file=amongwrite)
        amongwrite.close()
        await message.channel.send('Saved!')
    if 'seecode' in said:
        amongwrite = open('amongcode.txt', 'r')
        for line in amongwrite:
          code, server = line.rstrip().split(',')
        await message.channel.send(f'{server}\n{code.upper()}')
        amongwrite.close()
    if 'resettime' in said:
        amongfile = open('amongpeople.txt', 'r')
        personList = []
        for line in amongfile:
            line = line.rstrip()
            if ':' not in line:
                personList.append(line)
        amongfile.close()
        amongfile = open('amongpeople.txt', 'w')
        for person in personList:
            print(person, file=amongfile)
        amongfile.close()
        await message.channel.send('Reset time!')
    elif 'settime' in said:
        timetoplay = said.split(' ')[1]
        amongfile = open('amongpeople.txt', 'a')
        print(timetoplay, file=amongfile)
        amongfile.close()
        await message.channel.send(f'Set time to {timetoplay}')
    if 'addppl' in said:
        personList = said.split(' ')[1::]
        amongfile = open('amongpeople.txt', 'a')
        for person in personList:
            print(person, file=amongfile)
        amongfile.close()
        await message.channel.send(f'Added {len(personList)} people!')
    if 'resetppl' in said:
        amongfile = open('amongpeople.txt', 'w')
        amongfile.close()
        await message.channel.send('Reset!')
    if 'removeppl' in said:
        amongfile = open('amongpeople.txt', 'r')
        removeList = said.split(' ')
        personList = []
        for line in amongfile:
          line = line.rstrip()
          if line not in removeList:
              personList.append(line)
        amongfile.close()
        amongfile = open('amongpeople.txt', 'w')
        for person in personList:
            print(person, file=amongfile)
        await message.channel.send('Removed!')
    if 'showppl' in said:
        amongfile = open('amongpeople.txt', 'r')
        amongList = []
        timetoplay = '*no time set*'
        for line in amongfile:
            if ":" not in line:
                line = line.rstrip().title()
                amongList.append(line)
            else:
              timetoplay = line.rstrip()
        await message.channel.send(f'There are {len(amongList)} people playing at {timetoplay}:')
        await message.channel.send('\n'.join(amongList))
    if 'amongperson' in said:
        await message.channel.send('⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣛⣛⣛⣻⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣟⣿⡿⠟⠛⠛⠛⠛⠻⠿⣿⣿⡿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣟⣾⡏⠀⠀⠀⠀⠀⢀⣀⣀⣀⣹⣿⣯⢿⣿⣿⣿\n⣿⣿⣿⣿⣿⣽⡿⠀⠀⠀⣴⣿⠿⠛⠛⠛⠛⠛⠻⠿⣮⡿⣿⣿\n⣿⡿⢟⣿⣿⣿⡇⠀⠀⠀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣽⣿\n⣿⣼⡟⠛⠉⣿⠀⠀⠀⠀⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣟⣿\n⣧⣿⠃⠀⢰⣿⠀⠀⠀⠀⠘⢿⣷⣤⣄⣀⣀⣤⣴⣶⣿⣟⣿⣿\n⡿⣿⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠋⠉⠉⠀⣿⣿⣿⣿\n⣻⣿⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣿⣿\n⣿⣿⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣧⣿⣿\n⣿⣿⡀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢿⣿⣿\n⣿⡽⣷⣦⣤⣿⡆⠀⠀⠀⠀⣠⣤⣤⣀⣀⣀⠀⠀⢸⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⣿⡏⡍⣿⡏⠀⠀⠀⣿⡏⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⣿⡇⣷⣿⣇⣀⣀⣀⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣝⢿⣶⣶⣶⣾⢟⣳⣿⣷⣽⣿⣿⣯⣯⣿⣿⣿⣿')

    if 'amongeject' in said:
        a, person = said.split(' ')
        person = person.title()
        await message.channel.send(f'. 　　　。　　　　•　 　ﾟ　　。 　　.\n\n　　　.　　　 　　.　　　　　。　　 。　. 　\n\n.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•\n\n　　ﾟ　　    {person} was ejected .　 。　.\n\n　　　　　 1 Impostor remains 　 　　。\n\n　　ﾟ　　　.　　　. ,　　　　.　 .')





client.run(TOKEN)