import discord
from dtoken import TOKEN
from discord.ext import commands

client = commands.Bot(command_prefix="?")

# start-up
@client.event
async def on_ready():
    print("I might be in a bathing suit, but I can, and will, continue to maintain order.")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Dragalia Lost"))


@client.command()
async def notte(ctx):
    await ctx.send("Sweet sassy molassy!")

client.run(TOKEN)