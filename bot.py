from mcstatus import MinecraftServer
import discord
from discord.ext import commands
import json
import asyncio
import threading

bot = commands.Bot(command_prefix='>')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('BOT MADE BY GELLATIO (@femboychrist on twitter)')

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hello there! In order to get this bot setup, type ``>set IP Channel Role``, replacing IP with your server IP, replacing channel with what channel you want to send updates to, and replacing Role with what role you want me to tag when it does go down. If you don\'t want me to tag a role, simply type none.')
        break

@bot.command()
async def set(ctx, arg1, arg2, arg3):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send('Your server IP address is {}. The channel updates will be sent to is {}, and the role I will tag is {}.'.format(arg1, arg2, arg3))
        with open('config.json') as json_file:
            data = json.load(json_file)

            chanid = str(ctx.message.guild.id)
            data['data'][chanid] = {}
            data['data'][chanid]['ip'] = arg1
            data['data'][chanid]['channel'] = arg2
            data['data'][chanid]['role'] = arg3
            with open('config.json', 'w') as outfile:
                json.dump(data, outfile)
            with open('status.json') as status_file:
                alive = json.load(status_file)
                alive['data'][chanid] = {}
                alive['data'][chanid]['alive'] = True
                alive['data'][chanid]['sent'] = False
                with open('status.json', 'w') as outfile:
                    json.dump(alive, outfile)
@bot.command()
async def status(ctx):
    try:
        with open('config.json') as json_file:
            servdata = json.load(json_file)
            chanid = str(ctx.message.guild.id)

            try:
                server = MinecraftServer.lookup(servdata['data'][chanid]['ip'])
                status = server.status()
                await ctx.send("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
            except KeyError:
                await ctx.send("It appears your server is not configured correctly. Please redo the set command. Use >help to see the syntax.")
            except CommandInvokeError:
                await ctx.send("It appears your server is not configured correctly. Please redo the set command. Use >help to see the syntax.")
    except ConnectionRefusedError:
        await ctx.send("Server is down!")
@bot.command()
async def info(ctx):
    with open('config.json') as json_file:
        data = json.load(json_file)
        chanid = str(ctx.message.guild.id)

        try:
            await ctx.send("""Current server settings:
IP address: {0}
Update channel: {1}
Role to tag: {2}""".format(data['data'][chanid]['ip'],data['data'][chanid]['channel'],data['data'][chanid]['role']))
        except KeyError:
            await ctx.send("It appears your server is not configured correctly. Please redo the set command. Use >help to see the syntax.")
        except CommandInvokeError:
            await ctx.send("It appears your server is not configured correctly. Please redo the set command. Use >help to see the syntax.")
#Uncomment this and replace the numbers in ctx.message.author.id == 210273983898058752 with your user ID, if you want to have a command to set your bot's game
#@bot.command()
#async def setgame(ctx, arg):
#    if ctx.message.author.id == 210273983898058752:
#        game = discord.Game(arg)
#        await bot.change_presence(status=discord.Status.idle, activity=game)
#        await ctx.send("Game changed to {}".format(arg))

@bot.command()
async def help(ctx):
    await ctx.send("""```MCStatus Bot Commands
Prefix is >

set - Creates basic setup for server updates & status checks
  Syntax: >set ip channel role
  **Make sure to tag the channel & role/user correctly! You must be an Administrator in order to use this!!!**
status - Gets server's current status
info - Gets your current settings```""")

bot.run('CHANGE_ME_TO_YOUR_TOKEN')
