import discord
import math
import random
import asyncio
import time
import threading
import requests
import osrsbox
import urllib
import json
import pprint
from osrs_api import GrandExchange
from osrs_api import Item
from discord.ext import commands
from osrsbox import items_api
from osrsbox import monsters_api


# Fully deployable discord bot with easy to understand functions.
# Commands are accessed via the "." operator
# Example: .dice  <---sending this message in discord will start the dice roller
# Type .commands to see all available commands


# Before running, pip install discord.py in your terminal
# pip install osrs-api
# pip install osrsbox
# pip install requests
# pip install pprint
# pip install asyncio


# Sets command prefix
# i.e. If you change the '.' to '!' you would type !dice to start the dice roller
bot = commands.Bot(command_prefix='.')


# Users secret Token 
# Access by going into discord developer portal and clicking "bots" on left hand tab
TOKEN = "TOKEN"


# Sends a message in the terminal stating the connection was successful
@bot.event
async def on_ready():
    print("Bot Connected!")


# Dice command that uses the pseudo-random randint() function to roll a number.
@bot.command()
async def dice(ctx):
    min = 1
    max = 6


    await ctx.send("Would you like to roll the dice?")


    try:
        msg = await bot.wait_for('message', timeout = 10.0)


        if msg.content == "yes" or msg.content == "Yes" or msg.content == "Y" or msg.content == "y":
            diceRoll = random.randint(min, max)
            await ctx.send("You rolled a " + str(diceRoll) + ".")

        else:
            await ctx.send("Exiting dice roller")

    except asyncio.TimeoutError:
           await ctx.send("You took too long!")

# Uses the openweathermap API to grab weather for any zip code that a user enters
# To activate this, do the following:
# Go to https://openweathermap.org/api and sign up for "Current Weather Data" (it's free)
# Once done, head over to https://home.openweathermap.org/api_keys
# Copy and paste your key into the "KEY" variable, and enjoy
# You can call this 1,000 times in a 24 hour period unless you upgrade your account

@bot.command()
async def currentWeather(ctx):
    KEY = "KEY"
    await ctx.send("Enter the zipe code of the area you'd like the weather for...")


    try:
        msg = None
        msg = await bot.wait_for('message', timeout = 15.0)
        r = requests.get('https://api.openweathermap.org/data/2.5/weather?zip=' + msg.content + '&units=imperial&appid=' + KEY)
        theForecast = r.json()


        await ctx.send("The current temperature in " + theForecast['name'] + " is: " + str(theForecast['main']['temp']) + "F" +
        "\n" + "Weather Condition: "+ theForecast['weather'][0]['main'])
        await ctx.send("--------------------------------------------------------------")
        await ctx.send("Would you like more weather information?(Y/N)")


        decision = None
        decision = await bot.wait_for('message', timeout = 15.0)


        if(decision.content == 'y' or decision.content == 'Y' or decision.content == 'yes' or decision.content == "YES"):
            await ctx.send("Humidity: " + str(theForecast['main']['humidity']) + "%"
            + "\n" + "Air Pressure: " + str(theForecast['main']['pressure']) + "\n" +
            "Wind speed: " + str(theForecast['wind']['speed']) + " MPH" + "\n" + 
            "Low of the day: " + str(theForecast['main']['temp_min']) + "F" + "\n" +
            "High of the day: " + str(theForecast['main']['temp_max']) + "F")
        else:
            await ctx.send("Exiting weather application.")

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond, exiting weather application.")
    

    await ctx.send("Would you like to make another search? (Y/N)")
    keepgoing = None
    keepGoing = await bot.wait_for('message', timeout=10.0)
    if(keepGoing.content == "Y" or keepGoing.content == "y" or keepGoing.content == "yes" or keepGoing.content == 'YES'):
        await currentWeather(ctx)
    else:
        await ctx.send("Exiting")


# Imports the entire library of OSRS items
# You must spell the name EXACTLY how it's spelled in game!
# Example: Must type `Abyssal whip` instead of `Abyssal Whip`
# -----------------------------------------------------------
# Uses both the OSRS API and the OSRSBox API to provide item info and
# current Grand Exchange Price
@bot.command()
async def osrsItemLibrary(ctx):
    await ctx.send("Welcome to the OSRS Item Library.  Please enter the item you wish to search for: \n")
    itemSearch = await bot.wait_for('message' , timeout = 10.0)


    item_id = Item.get_ids(itemSearch.content)
    geLookup = GrandExchange.item(item_id)


    formattedItem = itemSearch.content.replace(" ", "%20")


    items = requests.get('https://api.osrsbox.com/items?where={"name":"' + formattedItem.capitalize() + '"}')
    itemjson = items.json()


    await ctx.send(itemjson['_items'][0]['name'] + "\n======================\n" + "Date of Release: " 
    + str(itemjson['_items'][0]['release_date']) + 
    '\n' + "Buy Limit: " + str(itemjson['_items'][0]['buy_limit']) + "\n" +
    "High Alch Value: " + str(itemjson['_items'][0]['highalch']) + "\n" +  
    "Wiki URL: " + str(itemjson['_items'][0]['wiki_url']) + "\n" +
    "Current GE Price: " + str(geLookup.price()) + "gp" + '\n')
    
    
    await ctx.send("Would you like to make another search? (Y/N)")
    keepgoing = None
    keepGoing = await bot.wait_for('message', timeout=10.0)
    if(keepGoing.content == "Y" or keepGoing.content == "y" or keepGoing.content == "yes" or keepGoing.content == 'YES'):
        await osrsItemLibrary(ctx)
    else:
        await ctx.send("Exiting")


# WARNING: THIS DELETES MESSAGES 
# !!!YOU MUST GRANT THIS BOT SERVER PERMISSIONS TO USE THIS!!!
# ------------------------------------------------------------
# This will permanently delete/purge messages from a channel
# BE CAREFUL! When prompted, enter the number of messages to be deleted,
# NOT INCLUDING YOUR OWN AND THE PROMPT!
@bot.command()
async def clearMessages(ctx):
    await ctx.send("How many messages would you like to purge?")
    amount = await bot.wait_for('message', timeout = 7.0)
    await ctx.channel.purge(limit= int(amount.content) + 3)


@bot.command()
async def commands(ctx):
    await ctx.send("List of commands: " + "\n" + "==================" + "\n" + 
    ".dice - A simple dice roller" + "\n" + "----------------------" + "\n" +
    ".currentWeather - Displays weather information based off of a user entered zip code" +
    '\n' + '-------------------\n' + ".osrsItemLibrary - Starts the OSRS Item Library to look up items" +
    '\n' + '-------------------\n' + ".clearMessages - Purge channel messages *REQUIRES SERVER PERMISSIONS*\n")


bot.run(TOKEN)