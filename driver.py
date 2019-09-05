# Chetra Mo
# Driver file for my Dragalia Lost-themed Discord bot - Estelle

import discord
from dtoken import TOKEN
from discord.ext import commands
import info_methods

MAX_LEVEL_TWO = "Description2"
MAX_LEVEL_THREE = "Description3"
bot = commands.Bot(command_prefix="?")


@bot.event
async def on_ready():
    print("I might be in a bathing suit, but I can, and will, continue to maintain order.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Dragalia Lost"))


@bot.command()
async def commands(ctx):
    """
    Displays a list of available commands.
    :param ctx: Context command was issued
    :return: None
    """
    file = open("commandsList.txt", "r")
    await ctx.send(file.read())
    file.close()


@bot.command()
async def info(ctx, *, arg: str):
    """
    Retrieves information about the adventurer/dragon and prints it to the Discord text channel.
    :param ctx: Context command was issued
    :param arg: String entered in by user containing entity name
    :return: None
    """
    entity = arg

    try:
        entityDict = info_methods.make_dict(entity)
    except AttributeError:
        await ctx.send(f"{entity} does not exist. Are you sure you spelled their name right?")
    else:
        if "adventurer" or "dragon" in entityDict:
            if entityDict["entityType"] == "adventurer":
                embed = discord.Embed(title="Adventurer", description=entityDict["FullName"], color=0x3D85C6)
                imageLink = info_methods.get_image(entityDict["entityType"], entityDict["Rarity"],
                                                   entityDict["Id"], entityDict["VariationId"])
                skillDescriptionOne = info_methods.pretty_print(entityDict["Skill1Name"],
                                                                info_methods.get_skill(entityDict["entityType"],
                                                                                       entityDict["Skill1Name"],
                                                                                       MAX_LEVEL_THREE))
                skillDescriptionTwo = info_methods.pretty_print(entityDict["Skill2Name"],
                                                                info_methods.get_skill(entityDict["entityType"],
                                                                                       entityDict["Skill2Name"],
                                                                                       MAX_LEVEL_TWO))
                footer = info_methods.get_footer(entityDict)
                embed.set_thumbnail(url=imageLink)
                embed.add_field(name="Skill 1", value=skillDescriptionOne, inline=False)
                embed.add_field(name="Skill 2", value=skillDescriptionTwo, inline=False)
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)
            elif entityDict["entityType"] == "dragon":
                embed = discord.Embed(title="Dragon", description=entityDict["FullName"], color=0x3D85C6)
                imageLink = info_methods.get_image(entityDict["entityType"], entityDict["Rarity"],
                                                   entityDict["BaseId"], entityDict["VariationId"])
                skillDescriptionOne = info_methods.pretty_print(entityDict["SkillName"],
                                                                info_methods.get_skill(entityDict["entityType"],
                                                                                       entityDict["SkillName"],
                                                                                       MAX_LEVEL_TWO))
                favoriteGift = info_methods.get_favorite(entityDict["FavoriteType"])
                footer = info_methods.get_footer(entityDict)
                embed.set_thumbnail(url=imageLink)
                embed.add_field(name="Skill", value=skillDescriptionOne, inline=False)
                embed.add_field(name="Favorite Gift", value=favoriteGift, inline=False)
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)


@bot.command()
async def notte(ctx):
    """
    Sends a fun message.
    :param ctx: Context command was issued
    :return: None
    """
    await ctx.send("Sweet sassy molassy!")


bot.run(TOKEN)
