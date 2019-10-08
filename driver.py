import discord
from dtoken import TOKEN
from discord.ext import commands
import info_methods

ADVENTURER = "adventurer"
DRAGON = "dragon"
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
    entity = arg.title()
    wordCount = entity.split()
    
    if len(wordCount) < 3:
        # check if adventurer or dragon exists first
        entityDict = info_methods.make_dict(entity)
        if entityDict is None:
            await ctx.send(f"'{entity}' does not exist (or you may have misspelled their name).")
        else:
            if entityDict["type"] == ADVENTURER:
                name = entityDict["name"].replace(" ", "_")
                emojiString = info_methods.get_adv_emojis(entityDict["rarity"], entityDict["element"],
                                                          entityDict["weapon"], entityDict["class"])
                embed = discord.Embed(title=entityDict["name"], description=emojiString, color=0x3D85C6)
                icon = discord.File(f"./adventurers/{name}.png", filename=f"{name}.png")
                embed.set_thumbnail(url=f"attachment://{name}.png")

                skillOneDescription = info_methods.print_skills(entityDict["skill_one"], entityDict["skill_one_desc"],
                                                                ADVENTURER)
                skillTwoDescription = info_methods.print_skills(entityDict["skill_two"], entityDict["skill_two_desc"],
                                                                ADVENTURER)
                abilities = info_methods.print_abilities([entityDict["ability_one"], entityDict["ability_two"],
                                                         entityDict["ability_three"]])

                embed.add_field(name="Skill 1", value=skillOneDescription, inline=False)
                embed.add_field(name="Skill 2", value=skillTwoDescription, inline=False)
                embed.add_field(name="Abilities", value=abilities, inline=False)
                embed.add_field(name="Co-ability", value=entityDict["co_ability"], inline=False)
                await ctx.send(file=icon, embed=embed)

            elif entityDict["type"] == DRAGON:
                name = entityDict["name"].replace(" ", "_")
                emojiString = info_methods.get_dragon_emojis(entityDict["rarity"], entityDict["element"])
                embed = discord.Embed(title=entityDict["name"], description=emojiString, color=0x3D85C6)
                icon = discord.File(f"./dragons/{name}.png", filename=f"{name}.png")
                embed.set_thumbnail(url=f"attachment://{name}.png")

                skillOneDescription = info_methods.print_skills(entityDict["skill_one"], entityDict["skill_one_desc"],
                                                                DRAGON)
                abilities = info_methods.print_abilities([entityDict["ability_one"], entityDict["ability_two"]])

                embed.add_field(name="Skill", value=skillOneDescription, inline=False)
                embed.add_field(name="Abilities", value=abilities, inline=False)
                await ctx.send(file=icon, embed=embed)
    else:
        await ctx.send(f"'{entity}' is not a valid name.")


@bot.command()
async def notte(ctx):
    """
    Sends a fun message.
    :param ctx: Context command was issued
    :return: None
    """
    await ctx.send("Sweet sassy molassy!")


bot.run(TOKEN)
