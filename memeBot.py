#!/usr/bin/env python
# Version: 3.6
# Author: David Moore
# Description: This program will go to the iFunny website and post the first 100 memes into a discord text channel unless given a different number.
# this functionality was embedded from a program I called "loopMemes", and can work by itself.

# THIS PROGRAM WILL NOT WORK WITHOUT REGISTERING A BOT ON THE DISCORD WEBSITE, AND ENTERING A TOKEN VALUE AT THE BOTTOM OF THE SCRIPT. (VERY LAST LINE)

# Commands: "!getMeme 10" will get only the first 10 memes from the iFunny featured websiteself.
# "!getMeme" will grab the first 100 memes from the iFunny featured page.
# "!stop" will logout the bot even during a task. (This was incase someone said !getMeme 9999999, and we wanted an emergency stop)

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
#for the loopMemes###############
import requests
import datetime
# BeautifulSoup is our web scraper that we use.
from bs4 import BeautifulSoup
#################################
Client = discord.Client()
client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):
    if message.content == '!stop': await client.logout()
    if message.content.upper().startswith("!GETMEME"):
        args = message.content.split(" ")
        await client.send_message(message.channel, "Here is a few memes :ok_hand:")
        # this is where we add the webscraper code from the loopMemes program
        #########################
        # loopMemes start

        # This is the starter Link for the Web Scraper
        gLink = 'https://ifunny.co/'
        data = requests.get(gLink)

        # load Web Page into BeautifulSoup
        soup = BeautifulSoup(data.text, 'html.parser')

        f = open("ifunny.html", "w")
        f.write(data.text)

        # looks at all img tags with a class of media__image
        image = soup.findAll('a',{'class':'media__preview'})

        Link = image[0]
        pageLink = Link['href']
        gLink = 'https://ifunny.co' + pageLink

        # if there is an argument it will try to make it a number and get that number of memes, else it defaults to 100
        try:
            numMeme = int(args[1])
        except:
            numMeme = 100

        i=0
        while i<numMeme:
            # Starting at the link
            data = requests.get(gLink)

            # load Web Page into BeautifulSoup
            soup = BeautifulSoup(data.text, 'html.parser')

            # looks at all img tags with a class of media__image
            image = soup.find('img',{'class':'media__image'})

            # Looks at only the data-src attribute from the img tag
            imgLink = image['data-src']

            # place the image in the text channel
            await client.send_message(message.channel,imgLink)

            # looks at all a tags with a class of media__control_next
            nextPage = soup.find('a',{'class','media__control_next'})

            # Looks at only the href attribute from the a tag
            pageLink = nextPage['href']

            # uses the <a> tag href attribute to go to the nextweb Page, and restart the loop
            gLink = 'https://ifunny.co' + pageLink

            i+=1
        # after loop display a message to know that it is over
        await client.send_message(message.channel,"I have finished your request.")
        #################################################################################################### loopMemes end
# Place your bot token below. This can be obtained from the discord website after you have registered a bot.
client.run("PLACE YOUR TOKEN HERE") # make sure not to post code with this value!!!
