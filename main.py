import discord
from discord.ext import commands
import os
import random
import time
import asyncio
import json
import requests
from requests import get
from json import loads


client = commands.Bot(
    command_prefix=commands.when_mentioned_or("."),
    case_insensitive=True,
    owner_id=353416871350894592)


intents = discord.Intents(messages=True, guilds=True)

intents.presences = True
intents.members = True


client.remove_command('help')


# ---- Cogs ----


@client.command()
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")



# ---- Events ----


@client.event
async def on_ready():
	print('Logged in as {0} ({0.id})'.format(client.user))


# @client.event
# async def on_command_error(ctx, error):
# 	if isinstance(error, commands.MissingRequiredArgument):
# 		embed = discord.Embed(
# 		    description=f"Please pass in all requirements", color=0xff0000)
# 		await ctx.send(embed=embed)
# 	if isinstance(error, commands.MissingPermissions):
# 		embed = discord.Embed(
# 		    description=f"You don't have the required permissions",
# 		    color=0xff0000)
# 		await ctx.send(embed=embed)
# 	if isinstance(error, commands.CommandOnCooldown):
# 		coold = str(time.strftime('%H:%M:%S', time.gmtime(error.retry_after)))
# 		embed = discord.Embed(
# 		    description=f"**{ctx.author}** Cooldown: {coold}",
# 		    color=0xff0000)
# 		await ctx.send(embed=embed)


client.run('')
