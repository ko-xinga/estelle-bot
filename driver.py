# Chetra Mo
# Driver file for my Dragalia Lost-themed Discord bot - Estelle

import discord
from dtoken import TOKEN
from discord.ext import commands
import info_methods

bot = commands.Bot(command_prefix="?")

# start-up (terminal)
@bot.event
async def on_ready():
    print("I might be in a bathing suit, but I can, and will, continue to maintain order.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Dragalia Lost"))

# ?notte sends a silly message
@bot.command()
async def notte(ctx):
    await ctx.send("Sweet sassy molassy!")

# ?info: sends an embedded Wiki entry about that character
# input: arg - string sent in by user
# output: sends embedded description of entity to discord channel the command was entered in
@bot.command()
async def info(ctx, *, arg: str):
    """
    Sends an embedded Wiki entry about that entity
    :param ctx: Context command was issued
    :param arg: String entered in by user containing entity name
    :return: None
    """
    entity = arg
    adventurerDict = {}
    print(entity)
    try:
        adventurerDict = info_methods.retrieve_dict(entity)
    except AttributeError:
        print("Inside except")
        await ctx.send(f"{entity} does not exist. Are you sure you spelled their name right?")
    else:
        embed = discord.Embed(title="Adventurer", description=adventurerDict["FullName"], color=0x3D85C6)
        embed.set_thumbnail(url="https://gamepedia.cursecdn.com/dragalialost_gamepedia_en/c/c5/110063_01_r04.png?version=012dea440c42c82f0f8bc86b9e5f5453")
        embed.add_field(name="Skill 1", value=adventurerDict["Skill1Name"], inline=False)
        embed.add_field(name="Skill 2", value=adventurerDict["Skill2Name"], inline=False)
        embed.set_author(name="Dragalia Lost Wiki", url="https://dragalialost.gamepedia.com")
        await ctx.send(embed=embed)


bot.run(TOKEN)