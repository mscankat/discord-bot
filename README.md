# discord-player-bot
A discord bot that downloads youtube music videos and streams them in discord channel


## What do we need?
- A discord account
- A discord bot
- The token of our discord bot
- Any environment that runs python




*(I am assuming you have a discord account)*

## How to create a discord bot?

- Sign in to discord in your browser
- [Click here](https://discord.com/developers) 
- Create a new application and give it a name

## How to get the token?

*It should give you the token when you first created the application but if you dont have one:*
- Go to bot section on the left
- Click `Reset Token`
- And you should have your new token

## How to invite our bot to our server?

- Go to OAuth2 > URL Generator on the left of the panel
- Check these following checkboxes:
    - application.commands
    - bot
    - connect
    - speak
    - Send Messages
  
  
  
*(Or you can just give it Administrator)*

- Go to the generated URL at the bottom 
- Select which server you want the bot to add

## How to hook the application to our python code?

- First, we have to edit our file to put our bots token:

Find this line in the code and put your token between the quotes:

`token = 'PUT YOUR TOKEN HERE'`

- Now we have to install the required libraries for our code to run:
    - `pip install discord.py`
    - `pip install yt_dlp`

## How to run the file?

- Open a terminal in the related directory
- Use `py discord-bot.py` or `python3 dioscord-bot.py`, depending on your OS

# What are the commands?

- ### `!join` 

This command makes the bot join the channel you are currently at

- ### `!play`

This command plays the desired song.

Example: `!play Imperial March`

You can use this command while the bot is already playing a music to add your musics to queue.

- ### `!skip`

Use this to skip the current music

- ### `!leave`

This command makes bot to leave the channel


- ### `!showq`

This command makes the bot to list the current queue

- ### `!clc`
The way that bot works is to download the music first then stream it to the discord channel and finally delete the music file.
So if it closes unexpectedly the music file won't be deleted. That's why we have this command to remove these files manually. You won't probably have to need that.

