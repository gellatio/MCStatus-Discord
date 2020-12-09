from mcstatus import MinecraftServer
import discord
from discord.ext import commands
import json
import asyncio
import threading

bot = commands.Bot(command_prefix='>>')

async def check_status():
    while True:
        with open('config.json') as json_file:
            serv = json.load(json_file)
            for i in serv['data']:
                try:
                    print(serv['data'][i]['ip'])

                    server = MinecraftServer.lookup(serv['data'][i]['ip'])
                    status = server.status()
                    print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
                    with open('status.json') as status_file:
                        alive = json.load(status_file)
                        alive['data'][i] = {}
                        alive['data'][i]['alive'] = True
                        alive['data'][i]['sent'] = False
                        with open('status.json', 'w') as outfile:
                            json.dump(alive, outfile)
                except ConnectionRefusedError:
                    with open('status.json') as status_file:
                        alive = json.load(status_file)
                        if alive['data'][i]['sent'] == False:
                            channelid = int(serv['data'][i]['channel'].strip('<').strip('#').strip('>'))
                            channel = client.get_channel(channelid)
                            if serv['data'][i]['role'] == "none":
                                await channel.send("The server {0} is currently down!".format(serv['data'][i]['ip']))
                            else:
                                await channel.send("The server {0} is currently down! {1}".format(serv['data'][i]['ip'],serv['data'][i]['role']))
                            alive['data'][i] = {}
                            alive['data'][i]['alive'] = False
                            alive['data'][i]['sent'] = True
                            with open('status.json', 'w') as outfile:
                                json.dump(alive, outfile)
                        if alive['data'][i]['sent'] == True:
                            alive['data'][i] = {}
                            alive['data'][i]['alive'] = False
                            alive['data'][i]['sent'] = True
                            with open('status.json', 'w') as outfile:
                                json.dump(alive, outfile)
                            print("The server is down, but the server has been notified.")
                await asyncio.sleep(10)



class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        await check_status()

client = MyClient()
client.run('CHANGE_ME_TO_YOUR_TOKEN')
