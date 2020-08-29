# discordBot
Custom Discord Bot written in Python.


This is a bot that you can use freely and easily modify within your discord server. 


Currently, this bot contains the following functionality:


* Dice roller - generates a pseudo-random number between min and max (1 and 6).
* Current Weather - Asks for the zip code of the area you'd like to get the weather for.  Shows basic information and then asks if the user would like a more detailed report
* OSRS Item Library - A library for every item in the popular game Oldschool Runescape.  Uses both the official OSRS API and OSRSBox to provide item information
* Commands - Shows the bots commands
* Clear Messages - This clears messages and is not shown on the command list. This should only be used by server mods/administrators


Prior to editing this for personal use, please make sure you have discord.py installed.  The other API's that have been imported via .py files are optional, but those used are:


* osrsbox
* json
* pprint
* asyncio
* The Open Weather API is used within the program, and there are instructions within the comments of the discordBot.py file on how to set up your own account to use this
