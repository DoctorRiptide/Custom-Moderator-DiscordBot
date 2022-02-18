# Imports #

import discord
from discord.ext import commands
from keep_alive import keep_alive
import schedule

"""
CHANGE THESE VARIABLES TO SUIT YOUR SERVER
"""

moderatorChannel = 'moderation'

adminRole = ["Admin", "admin"]

verifiedRole = 'verified'

prefix = '+'

CLIENT_SECRET = 'Client secret goes here'

"""
END OF CHANGEABLE VARS
"""

intents = discord.Intents.all()

intents.members = True

Client = discord.Client()

client = commands.Bot(command_prefix = [prefix], intents=intents)

""" Events """

# On member join

@client.event
async def on_member_join(member):
  await captcha(ctx=member)

# On ready

@client.event
async def on_ready():
  print("Ready")

# On message

@client.event
async def on_message(ctx):

  await client.process_commands(ctx)

  if 'Direct Message' in str(ctx.channel):
    return

  if ctx.channel.guild == None:
    return

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

  ch1 = discord.utils.get(
    ctx.guild.channels, 
    name=str(ctx.channel)
    )

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

# On message edit

@client.event
async def on_message_edit(message_before, message_after):

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
    title = "Message Delete",
    description = f'Author : {message.author} ::: Channel {message.channel.mention}',
    color = 0xe74c3c
    )

  embed.add_field(
    name = 'Message Deleted : ',
    value = message.content
    )

  channel = discord.utils.get(
    message.guild.channels,
    name = moderatorChannel
    )

  await channel.send(embed=embed)


@client.command()
async def purgeRoutine(ctx):

  for member in ctx.guild.members:

    role = discord.utils.get(
      ctx.guild.roles, 
      name=verifiedRole
      )

    user = discord.utils.get(
      ctx.guild.members, 
      name=member.name
      )

    if role in user.roles:
      continue

    else:
      ctx.guild.kick(user)

      user.send("You have been kicked for failing to verify")

      print(f'{user} has been kicked')

"""
Commands
"""

# Captcha Command

@client.command()
async def captcha(ctx):

  print('Captcha Occured')

  guild = ctx.guild

  user = ctx

  print(user)

  role1 = discord.utils.get(
    ctx.guild.roles, 
    name=verifiedRole)

  if role1 in ctx.roles:
    return

  await user.send("https://cdn.discordapp.com/attachments/943967436905009235/944051776468971520/unknown.png")

  await user.send("Please select an option. If answered correctly you will be verified - if not, you will be kicked. Feel free to check out physix.world")

  response = await client.wait_for('message')

  if response.author == client.user:
    response = await client.wait_for('message')

  if str(response.content.lower()) == 'a':
    await user.send("Correct! You have now been verified and given a role to prove it ;)")

    role = discord.utils.get(
      ctx.guild.roles, 
      name=verifiedRole
      )
    
    if role == None:
      await guild.create_role(name=verifiedRole)

    await user.add_roles(role)

    print("Role added")

  else:
    await user.send('Man, you got that incorrect. Maybe check out the website and familiarise yourself with https://physix.world before you join. You will now be kicked. Try again later :(')

    await guild.kick(user)

    print(f'Kicked {user}')

# Give everyone the verified role

@client.command()
@commands.has_permissions(administrator=True)
async def captcha_all(ctx):

  for member in ctx.guild.members:
    role = discord.utils.get(
      ctx.guild.roles, 
      name = verifiedRole
      )

    await member.add_roles(role)

"""
Schedules
"""

schedule.every().day.at("00:00").do(purgeRoutine)

keep_alive()
client.run(CLIENT_SECRET)
