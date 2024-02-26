import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from gtts import gTTS
from datetime import datetime
import os
import asyncio
from keep_alive import keep_alive 

keep_alive()
ffmpegOptions = {'options': "-vn"}

os.system('clear')

class color():
    green = '\033[92m'
    pink = '\033[95m'
    red = '\33[91m'
    yellow = '\33[93m'
    blue = '\33[94m'
    gray = '\33[90m'
    reset = '\33[0m'
    bold = '\33[1m'
    italic = '\33[3m'
    unline = '\33[4m'

bot = commands.Bot(command_prefix=',', intents=discord.Intents.all())
bot.remove_command('help')
voice = None
playing = False

@bot.event
async def on_ready():
    print(f'{color.gray+ color.bold}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {color.blue}CONSOLE{color.reset}  {color.pink}discord.on_ready{color.reset} Đã đăng nhập bot {color.bold}{bot.user}{color.reset}')
    try:
        sync = await bot.tree.sync()
        print(f'{color.gray+ color.bold}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {color.blue}CONSOLE{color.reset}  {color.pink}discord.command{color.reset} {len(sync)} commands')

    except Exception as e:
        print(e)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='Đen\'s playlist'))

async def send_welcome_message(channel, message):
    try:
        await channel.send(message)
    except Exception as e:
        print(e)

@bot.event
async def on_voice_state_update(member, before, after):
    global voice
    if voice is None:
        return

    if len(voice.channel.members) > 1:
        if member == bot.user:
            await send_welcome_message(voice.channel, f"Ô mai ca {member.name} vừa tham gia phòng nè, đè ra tẩn thôi.")
            return

    if before.channel != after.channel:
        if after.channel is not None:
            if member == bot.user:
                return
            await send_welcome_message(after.channel, f"Ô mai ca {member.name} vừa tham gia phòng kìa, đè ra tẩn thôi.")
            await welcome_message(after.channel)
        if before.channel is not None:
            if member == bot.user:
                return
            await send_welcome_message(before.channel, f" {member.name} vừa bỏ nhà đi bụi.")

async def welcome_message(channel):
    try:
        global voice
        voice = await channel.connect()
        tts = gTTS(text="Xin chào mọi người, chúc mừng các bạn đã tham gia voice chat!", lang='vi')
        tts.save("welcome.mp3")
        voice.play(FFmpegPCMAudio("welcome.mp3"))
        while voice.is_playing():
            await asyncio.sleep(1)
        await voice.disconnect()
        os.remove("welcome.mp3")
    except Exception as e:
        print(e)

@bot.command(name='s')
async def s(ctx, *, arg:str):
    global ffmpegOptions, voice, playing

    if not arg:
        return

    if ctx.message.author.voice is None:
        await ctx.send('Tạo room voicechat đê!')
        return

    if ctx.guild.voice_client is None:
        try:
            voice = await ctx.message.author.voice.channel.connect()
        except Exception as e:
            print('error', e)
            return
    elif ctx.guild.voice_client.channel != ctx.message.author.voice.channel:
        await ctx.send('Đang đi chơi với zai rồi!')
        return

    if playing == False:
        gTTS(text=arg, lang='vi').save('tts-audio.mp3')
        playing = True
        voice.play(FFmpegPCMAudio('tts-audio.mp3', **ffmpegOptions, executable='ffmpeg'), after=PlayingFalse)

    else:
        await ctx.send('Cào phím chậm thôi!')

@bot.command(name='leave')
async def leave(ctx):
    global voice
    if ctx.guild.voice_client is None:
        await ctx.send('Tạo room voicechat đê!')
        return

    if ctx.message.author.voice is None:
        await ctx.send('Bot không có ở trong vc!')
        return

    if ctx.message.author.voice.channel != ctx.guild.voice_client.channel:
        await ctx.send('Đang đi chơi với zai rồi!')
        return

    voice.stop()
    await ctx.guild.voice_client.disconnect()
    await ctx.send(f'để tôi cút cho bạn vừa lòng **{ctx.message.author.voice.channel.name}**')

def PlayingFalse(error):
    global playing
    playing = False

bot.run(os.environ.get('TOKEN'))