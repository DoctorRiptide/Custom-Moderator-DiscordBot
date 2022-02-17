# Imports #

import discord
from discord.ext import commands
from keep_alive import keep_alive
import time

# Code #

"""
CHANGE MODERATOR CHANNEL HERE
"""

moderatorChannel = 'moderation'

"""
MODERATOR CHANNEL ABOVE
"""

adminRole = ["Admin", "admin"]

Client = discord.Client()

client = commands.Bot(command_prefix = ["+"])

client.remove_command(name='help')

""" Events """

@client.event
async def on_ready():

  print(f'Admin role: {adminRole} \n Logged in as: {client.user.name} \n Bot ID: {str(client.user.id)}')

  for guild in client.guilds:
    print("Connected to server: {}".format(guild))
		
@client.event
async def on_message(ctx):

  if ctx.content.startswith('help'):
    await ctx.channel.send("Try using the help command (+help)")

  """ Message Log. Setup to record all messages to the channel messgae-log - Can be changed."""

  channel=discord.utils.get(
    ctx.guild.channels,
    name=moderatorChannel
  )

  if ctx.author == client.user:
    return

  if channel == None:
    return
  
  fullMessage = "**Message Content : ** *" + ctx.content + '*'
  ch1 = discord.utils.get(ctx.guild.channels, name=str(ctx.channel))

  embed=discord.Embed(
    title=str(ctx.author), 
    description=fullMessage,
    color = 0x2ecc71)

  embed.add_field(
    name="Message Channel",
    value=ch1.mention,
    inline=False
  )

  if ctx.channel == channel:
    return

  await channel.send(embed=embed)

  await client.process_commands(ctx)

@client.event
async def on_reaction_add(reaction, user):

  """ Retrieve discord objects for usage """

  channel = discord.utils.get(
    user.guild.channels,
    name="verify"
  )

  role = discord.utils.get(
    user.guild.roles,
    name="verified"
  )

  """ Checks """

  if channel == None:
    return 

  if reaction.message.channel != channel:
    print(reaction.message.channel)
    print(channel)
    return

  await user.add_roles(role)

@client.event
async def on_message_edit(message_before, message_after):
  embed = discord.Embed(title = "Message Edit",
  description = f'Channel : {message_after.channel.mention} ::: Author : {message_before.author.mention}',
  color = 0xe67e22)

  embed.add_field(name = 'Message Before',
  value = message_before.content)

  embed.add_field(name = 'Message After',
  value = message_after.content)

  channel = discord.utils.get(message_before.guild.channels, name = moderatorChannel)

  await channel.send(embed=embed)

@client.event
async def on_message_delete(message):

  embed = discord.Embed(title = "Message Delete",
  description = f'Author : {message.author} ::: Channel {message.channel.mention}',
  color = 0xe74c3c)

  embed.add_field(name = 'Message Deleted : ',
  value = message.content)

  channel = discord.utils.get(message.guild.channels, name = moderatorChannel)

  await channel.send(embed=embed)
    
""" Commands """

@client.event
async def on_member_join(member):
  embed = discord.Embed(title = member.author,
  description = 'Joined Server',
  color = 0x2ecc71)

  channel = discord.utils.get(member.guild.channels, name = moderatorChannel)

  await channel.send(embed=embed)

@client.command(aliases=['helps'])
async def help(ctx):
  embed = discord.Embed(
    title="Help",
    description = "A list of usable commands and their purposes")
  embed.add_field(
    name='+verify',
    value='Will completely remove the selected channels messgages and remove the permission for anyone without the verify role to speak in any other channel (excluding admins). Please ensure that all the other wanted channels allow people with the verify role to speak / interact.' 
  )
  embed.add_field(
    name="+clear messageAmount",
    value="Deletes messages with a provided message amount.",
    inline=True
  )
  await ctx.channel.send(embed=embed)
	
@client.command(aliases=["purge", "delete"])
@commands.has_permissions(administrator=True)
async def clear(ctx, *, length=100):

  await ctx.channel.send("Hey, im clearing {} messages!".format(length))

  time.sleep(2)

  await ctx.channel.purge(limit=int(length))

@client.command(aliases=["verification"])
@commands.has_permissions(administrator=True)
async def verify(ctx, *, channelNameInput=None):

  if channelNameInput == None:
    channel = discord.utils.get(
    ctx.guild.channels,
    name="verify"
  )

  else:
    channel = discord.utils.get(
      ctx.guild.channels,
      name=channelNameInput
    )

  if channel == None:
    await ctx.channel.edit(name="verify")
    channel = ctx.channel

  await clear(ctx, length=100000)

  # Create role check & set perms #

  role = discord.utils.get(
    ctx.guild.roles,
    name="verified"
    )

  if role == None:
    await ctx.guild.create_role(name="verified")

    role = discord.utils.get(
    ctx.guild.roles,
    name="verified"
    )

  for channel1 in ctx.guild.channels:
    if channel1 == channel:
      continue
    else:
      await channel1.set_permissions(ctx.guild.default_role, view_channel=False)

  """ Setup permissions """

  await channel.set_permissions(
    ctx.guild.default_role,
    send_messages=False
  )

  await channel.send("Hey newcomer! Please react here to verify yourself to access all the other channels. :smiley:")

keep_alive()    
client.run('TOKEN GOES HERE')
