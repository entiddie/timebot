import discord
from discord.ext import commands
import json
import requests
import time
from pymongo import MongoClient
import asyncio


uri = "mongodb+srv://user:pw@cluster0.ieseb.mongodb.net/db?retryWrites=true&w=majority"

cluster = MongoClient(uri)

db = cluster['tz']
col = db['tz']


class Set(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def tzset(self, ctx, *, location = None):

        authid = ctx.author.id

        if not location:
            ...
            return
        
        if col.count({'userid': authid}) == 0:
            post = {"userid": authid, "location" : location}
            col.insert_one(post)

            await ctx.send(f"Set")

        else:
            myquery = {"userid": authid}
            newvalues = {"$set": {'location': location}}

            col.update_one(myquery, newvalues)
            
            await ctx.send("Set")



        
def setup(client):
    client.add_cog(Set(client))
