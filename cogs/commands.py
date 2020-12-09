import discord
from discord.ext import commands
import json
import requests
import time
from pymongo import MongoClient
import asyncio
from datetime import datetime
import pytz


uri = "mongodb+srv://user:pw@cluster0.ieseb.mongodb.net/db?retryWrites=true&w=majority"

cluster = MongoClient(uri)

db = cluster['tz']
col = db['tz']


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong! {round(ping)}ms")


    @commands.command()
    async def time(self, ctx, *, place: str = None):

        if not place:

            authid = ctx.author.id

            if col.count({'userid': authid}) == 0:
                em = discord.Embed(
                    color=0xfffafa,
                    description="""
To search the time for a particular location, specify the location name as follows
Usage: `.time [location]`
Example: `.time London`

To get time instantly for you, use the following command to set your default location
Usage: `.tzset [location]`
Example: `.tzset London`
    """
                )

                em.set_author(name="World Time", icon_url="https://i.imgur.com/ADqPmoB.png")

                await ctx.send(embed=em)
                return

            else:

                try:

                    results = col.find({"userid": authid})

                    for r in results:
                        result = r

                    place = r['location']

                    response = requests.get(
                        "https://timezone.abstractapi.com/v1/current_time?api_key=d530aa97db5549588284aca1c8e9e8ba&location=" + place).json()

                    time = str(response['datetime'])

                    time = time.split(" ")

                    await ctx.send(f"**{ctx.author.display_name}:** {time[1]}")
                    
                    return

                except:
                    await ctx.send(f"No locations found by the name **'{place}'**")
                    return


        try:
            response = requests.get(
                "https://timezone.abstractapi.com/v1/current_time?api_key=d530aa97db5549588284aca1c8e9e8ba&location=" + place).json()

            em = discord.Embed(
                color=0xfffafa,
                description=f"""
        DateTime: **{response['datetime']}**
        Timezone: {response['timezone_name']} ({response['timezone_abbreviation']})
        Timezone Location: {response['timezone_location']}
        """
            )

            em.set_author(name=f"Time — {str(response['requested_location']).capitalize()}", icon_url="https://i.imgur.com/ADqPmoB.png")

            await ctx.send(embed=em)

        except:
            await ctx.send(f"No locations found by the name **'{place}'**")
            return


    @commands.command()
    async def world(self, ctx):
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY)
        ny = datetime_NY.strftime("%H:%M:%S")

        tz_London = pytz.timezone('Europe/London')
        datetime_London = datetime.now(tz_London)
        lnd = datetime_London.strftime("%H:%M:%S")

        tz_Delhi = pytz.timezone('Asia/Kolkata')
        datetime_Delhi = datetime.now(tz_Delhi)
        de = datetime_Delhi.strftime("%H:%M:%S")

        tz_Jap = pytz.timezone('Asia/Tokyo')
        datetime_Japan = datetime.now(tz_Jap)
        jp = datetime_Japan.strftime("%H:%M:%S")

        tz_Sydney = pytz.timezone('Australia/Sydney')
        datetime_Sy = datetime.now(tz_Sydney)
        sy = datetime_Sy.strftime("%H:%M:%S")

        tz_Ch = pytz.timezone('Asia/Shanghai')
        datetime_Ch = datetime.now(tz_Ch)
        ch = datetime_Ch.strftime("%H:%M:%S")

        em = discord.Embed(color=0xfffafa, title=":earth_americas: World")

        em.add_field(name="New York", value=ny)
        em.add_field(name="London", value=lnd)
        em.add_field(name="New Delhi", value=de)
        em.add_field(name="Tokyo", value=jp)
        em.add_field(name="Sydney", value=sy)
        em.add_field(name="China", value=ch)

        await ctx.send(embed=em)


    @commands.command(aliases=['timezone'])
    async def tz(self, ctx, timezone: str = None):
        if not timezone:
            em = discord.Embed(color=0xfffafa,
                description="Searching the time for a specific timezone\n\nUsage: `.tz [timezone]`\nExample: `.tz Asia/Tokyo`"
            )

            em.set_author(name="Time for specific timezones", icon_url=self.client.user.avatar_url)

            em.set_footer(text="Use .zones to get a list of all valid timezones")

            await ctx.send(embed=em)
            return
        
        try:
            tz = pytz.timezone(timezone)

            time = datetime.now(tz)

            time = str(time)[:-13]

            objects = time.split()

            await ctx.send(f"{objects[0]} **{objects[1]}**")

        except:
            await ctx.send(f"**'{timezone}'** is not a valid timezone")

    @commands.command(aliases=['av', 'avy'])
    async def avatar(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        em = discord.Embed()

        em.set_author(name=f"{member}", icon_url=member.avatar_url)

        em.set_image(url=member.avatar_url)

        await ctx.send(embed=em)


    @commands.command()
    async def help(self, ctx):
        em = discord.Embed(color=0xfffafa, description="""
**All my commands start with .**

**Basic**
.ping - Ping the bot
.avatar - User Avatar
.help - Sends this help page

**Time**
.time [location/none] - Time for a location / time at your location if set
.world - Time for major cities
.zones - Big list of all available timezones
.tz [timezone] - Time for a timezone

**Personalize**
.tzset [location] - Set your location to get time instantly
""")
        
        em.set_author(name="Timezone Help", icon_url=self.client.user.avatar_url)

        await ctx.send(embed=em)



        
def setup(client):
    client.add_cog(Commands(client))
