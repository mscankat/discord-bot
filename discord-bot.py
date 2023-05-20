import os
import discord
import asyncio
from discord.ext import commands
from yt_dlp import YoutubeDL
from discord import FFmpegPCMAudio
import glob

# Global variables
queue = []  # Music queue
voice_client = None  # Voice client for the bot

# Set up the Discord bot
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

#Put your bots token below
token = 'PUT YOUR TOKEN HERE'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_voice_state_update(member, before, after):
    global voice_client
    # Check if the bot joined a voice channel
    if member.id == bot.user.id and after.channel is not None:
        voice_client = await after.channel.connect()


@bot.command()
async def join(ctx):
    global voice_client
    # Join the voice channel of the user who issued the command
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()


@bot.command()
async def leave(ctx):
    global voice_client
    # Leave the voice channel
    voice_client = ctx.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()

@bot.command()
async def skip(ctx):
    global voice_client
    # Skip the current song and play the next one in the queue
    if voice_client.is_playing():
        voice_client.stop()
        await play_queue(ctx)




@bot.command()
async def clc(ctx):
    files = glob.glob('/usr/local/downloads/*')
    print(files)
    for f in files:
        os.remove(f)

 
@bot.command()
async def play(ctx, *, query):
    global queue, voice_client
    if voice_client == None:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()
    
    # Download the audio from the YouTube video using YoutubeDL
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True
    }
    
    # Search for videos on YouTube using youtube-dlp
    with YoutubeDL(ydl_opts) as ydl:
        if query.startswith('http'):
            info_dict = ydl.extract_info(query, download=False)
        else:
            info_dict = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]

        video_url = f"https://www.youtube.com/watch?v={info_dict['id']}"
        ydl.download([video_url])

    queue.append({'url': video_url, 'title': info_dict['title']})

    print(info_dict['id'])

    if not voice_client.is_playing():
        await play_queue(ctx)
    else:
        await ctx.send(f'Queued: {info_dict["title"]}')


async def play_queue(ctx):
    global queue, voice_client
    # Play the next song in the queue
    if len(queue) > 0:
        video = queue.pop(0)
        await ctx.send(f'Now playing: {video["title"]}')
        audio_file = f'downloads/{video["url"].split("=")[-1]}.mp3'
        voice_client.play(FFmpegPCMAudio(audio_file), after=lambda e: asyncio.run_coroutine_threadsafe(play_queue(ctx), bot.loop))
        
        while voice_client.is_playing():
            await asyncio.sleep(1)
        os.remove(audio_file)

@bot.command()
async def showq(ctx):
    global queue, voice_client
    q = []
    for song in queue:
        q.append(song['title'])
    
    songs = '\n'.join(q)
    await ctx.send(songs)
    

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send(f'Error: {str(error)}')


# Run the bot
bot.run(token)
