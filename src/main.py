# Imports #

import discord
from discord.ext import commands
from keep_alive import keep_alive

"""
CHANGE THESE VARIABLES TO SUIT YOUR SERVER
"""

moderatorChannel = 'moderation'

adminRole = ["Admin", "admin"]

verifiedRole = 'verify'

prefix = '+'

welcomeChannel = 'welcome'

"""
END OF CHANGEABLE VARS
"""

intents = discord.Intents.all()

intents.members = True

Client = discord.Client()

client = commands.Bot(command_prefix = [prefix], intents=intents)

client.remove_command(name='help')

"""
Help Command
"""
@client.command()
async def help(ctx):

  embed = discord.Embed(
    title = "Help",
    description = "Prefix : ***{}*** \n Verified Role : ***{}*** \n Moderator Channel : ***{}*** \n Admin Roles : ***{}***".format(prefix, verifiedRole, moderatorChannel, adminRole),
    color = 0x2ecc71
  )

  embed.add_field(
    name = "Logging (Not a command)",
    value = "Logging all messages, edits, deletes etc in {}".format(moderatorChannel),
    inline = False
  )
  
  embed.add_field(
    name = f'{prefix}clear 100',
    value = "Will clear a set amount of messages",
    inline = False
  )

  embed.add_field(
    name = f'{prefix}captcha_all',
    value = 'Will give all members of the guild the verified role',
    inline = False
  )

  embed.add_field(
    name = f'{prefix}purge_routine',
    value = 'Will kick all without the verified role',
    inline = False
  )

  await ctx.channel.send(embed=embed)


""" Events """

# On ready

@client.event
async def on_ready():
  print("Ready")

# On member join

@client.event
async def on_member_join(member):

  await captcha(ctx=member)

  channel = discord.utils.get(
    member.guild.channels,
    name = welcomeChannel
  )

  modChannel = discord.utils.get(
    member.guild.channels,
    name = moderatorChannel
  )

  if channel == None:
    channel = discord.utils.get(
    member.guild.channels,
    name = 'general'
  )

  embed = discord.Embed(
    title = "Welcome!",
    description = "Welcome {} to SupraVision! Familiarise yourself with our goals and objectives at https://physix.world - Don't forget to verify! **You have 120 seconds to verify** ".format(member.mention),
    color = 0x2ecc71
  )
  
  await channel.send(embed=embed)

  if modChannel != None:
    await modChannel.send(embed=embed)

# On member leave

@client.event
async def on_member_remove(member):

  channel = discord.utils.get(
    member.guild.channels,
    name = welcomeChannel
  )

  modChannel = discord.utils.get(
    member.guild.channels,
    name = moderatorChannel
  )

  if channel == None:
    channel = discord.utils.get(
    member.guild.channels,
    name = 'general'
    )

  embed = discord.Embed(
    title = "Member Leave",
    description = f'{member.name} Left {member.guild.name}',
    color = 0x2ecc71
  )

  await channel.send(embed=embed)

  if modChannel != None:
    await modChannel.send(embed=embed)


# On message

@client.event
async def on_message(ctx):

  await client.process_commands(ctx)

  if 'Direct Message' in str(ctx.channel):
    return

  if ctx.channel.guild == None:
    return

  if ctx.content.startswith('help'):
    await ctx.channel.send(f'Try using the {prefix}help command!')

  """ Message Log. Setup to record all messages to the channel messgae-log - Can be changed."""

  channel=discord.utils.get(
    ctx.guild.channels,
    name=moderatorChannel
  )

  if ctx.author == client.user:
    return

  if channel == None:
    return

  ch1 = discord.utils.get(
    ctx.guild.channels, 
    name=str(ctx.channel)
    )

  print(ctx.content)

  embed=discord.Embed(
    title=str(ctx.author), 
    description=str(ctx.content),
    color = 0x2ecc71
    )

  embed.add_field(
    name="Message Channel",
    value=ch1.mention,
    inline=False
  )

  if ctx.channel == channel:
    return

  await channel.send(embed=embed)

# On message edit

@client.event
async def on_message_edit(message_before, message_after):

  if 'Direct Message ' in str(message_before.channel):
    return

  embed = discord.Embed(
    title = "Message Edit",
    description = f'Channel : {message_after.channel.mention} ::: Author : {message_before.author.mention}',
    color = 0xe67e22
    )

  embed.add_field(
    name = 'Message Before',
    value = message_before.content
    )

  embed.add_field(
    name = 'Message After',
    value = message_after.content
    )

  channel = discord.utils.get(
    message_before.guild.channels, 
    name = moderatorChannel
    )

  await channel.send(embed=embed)

# On message delete

@client.event
async def on_message_delete(message):

  embed = discord.Embed(
    title = "Message Deleted",
    description = f'Channel : {message.channel.mention} ::: Author {message.author}',
    color = 0xe74c3c
    )

  content1 = ':' + str(message.content)

  if message.content != None:
    embed.add_field(
      name = 'Content : ',
      value = str(content1)
    )

  channel = discord.utils.get(
    message.guild.channels,
    name = moderatorChannel
    )

  await channel.send(embed=embed)

# On role create

@client.event
async def on_guild_role_create(role):

  embed = discord.Embed(
    title = "Role Created",
    description = f'Role **{role.name} created!',
    color = 0x2ecc71
  )

  channel1 = discord.utils.get(
    role.guild.channels,
    name = moderatorChannel
  )

  await channel1.send(embed=embed)

# On role delete

@client.event
async def on_guild_role_delete(role):

  embed = discord.Embed(
    title = "Role Deleted",
    description = f'Role **{role.name} deleted!',
    color = 0xe74c3c
  )

  channel1 = discord.utils.get(
    role.guild.channels,
    name = moderatorChannel
  )

  await channel1.send(embed=embed)

# On role update

@client.event
async def on_guild_role_update(role_before, role_after):

  embed = discord.Embed(
    title = "Role Update",
    description = f'Role changed from **{role_before}** to **{role_after}**',
    color = 0xe67e22
  )

  channel1 = discord.utils.get(
    role_after.guild.channels,
    name = moderatorChannel
  )

  await channel1.send(embed=embed)

# On member ban

@client.event
async def on_member_ban(guild, user):

  embed = discord.Embed(
    title = "Member Banned",
    description = f'{user.name} has been banned!',
    color = 0xe74c3c
  )

  channel1 = discord.utils.get(
    guild.channels,
    name = moderatorChannel
  )

  await channel1.send(embed=embed)

# On member ban

@client.event
async def on_member_unban(guild, user):

  embed = discord.Embed(
    title = "Member Unbanned",
    description = f'{user.name} has been unbanned!',
    color = 0x2ecc71
  )

  channel1 = discord.utils.get(
    guild.channels,
    name = moderatorChannel
  )

  await channel1.send(embed=embed)

"""
Commands
"""

# Clear

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, limit=100):

  await ctx.channel.send("Clearing {} messages :)".format(limit))

  limit = int(limit) + 1

  await ctx.channel.purge(limit=limit)
  
keep_alive()
client.run(CLIENT_SECRET)
