import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import datetime
from keepAlive import keep_alive

Client = discord.Client()
client = commands.Bot(command_prefix = ["$"])

@client.event
async def on_ready():
	print("Bot is ready!")
	print("Logged in as: " + client.user.name)
	print("Bot ID: " + str(client.user.id))
	for guild in client.guilds:
		print ("Connected to server: {}".format(guild))
	print("------")
		
@client.event
async def on_message(ctx):
  guild = ctx.guild
  channel1 = discord.utils.get(ctx.guild.channels, name="message-log")
  if channel1 == None:
    await ctx.channel.send("Please create a **message-log** text channel to log all messages")
  fullMessage = "**Message Content : **" + ctx.content
  embed = discord.Embed(title = str(ctx.author), description = )
  
    
keep_alive()
client.run('TOKEN HERE')
