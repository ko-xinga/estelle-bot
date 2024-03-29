import discord
from dtoken import TOKEN
from discord.ext import commands
import info_methods
import wp_methods
import findwp_methods
import manaspiral_methods
import emojis
import string
import unidecode

ADVENTURER = "adventurer"
DRAGON = "dragon"
MAX_LEVEL_TWO = "Description2"
MAX_LEVEL_THREE = "Description3"
bot = commands.Bot(command_prefix="?")
bot.remove_command("help")
BOT_CHANNEL = 605438885207736345

print("Program now running...")


@bot.event
async def on_ready():
    print("Estelle-bot is now running.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("?commands"))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"You need to include the name of the adventurer, dragon, or wyrmprint after the command. "
                       f"For example: `?(insert command here) Estelle`.")


@bot.command(aliases=["command", "commands", "help"])
async def list_commands(ctx):
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
    entity = string.capwords(arg)
    wordCount = entity.split()
    
    if len(wordCount) < 4:
        entityDict = info_methods.make_dict(entity)

        # check if adventurer or dragon exists first
        if entityDict is None:
            alternativeNames = info_methods.find_alternatives(entity)
            prettyString = info_methods.print_alternatives(alternativeNames)
            await ctx.send(f"'{entity}' does not exist in my database (or you may have misspelled their name). "
                           f"{prettyString}")
        else:
            # entity is an adventurer
            if entityDict["type"] == ADVENTURER:
                hasTwoSkills = True
                name = entityDict["name"].replace(" ", "_")
                emojiString = info_methods.get_adv_emojis(entityDict["rarity"], entityDict["element"],
                                                          entityDict["weapon"], entityDict["class"],
                                                          entityDict["mana_spiral"])
                embed = discord.Embed(title=entityDict["name"], description=emojiString, color=0x3D85C6)
                icon = discord.File(f"./adventurers/{name}.png", filename=f"{name}.png")
                embed.set_thumbnail(url=f"attachment://{unidecode.unidecode(name)}.png")

                formattedName = name.replace(" ", "_")
                skillOneDescription = info_methods.print_skills(entityDict["skill_one"], entityDict["skill_one_desc"],
                                                                ADVENTURER)
                if entityDict["skill_two"] == "-" and entityDict["skill_two_desc"] == "-":
                    hasTwoSkills = False
                skillTwoDescription = info_methods.print_skills(entityDict["skill_two"], entityDict["skill_two_desc"],
                                                                ADVENTURER)
                abilities = info_methods.print_abilities([entityDict["ability_one"], entityDict["ability_two"],
                                                         entityDict["ability_three"]])

                if len(skillOneDescription) > 1024:
                    embedCharLimit = "(This character's skill description exceeds Discord's character limit. " \
                                     "Please see the wiki link below for the full description.)"
                    embed.add_field(name="Skill 1", value=embedCharLimit, inline=False)
                else:
                    embed.add_field(name="Skill 1", value=skillOneDescription, inline=False)

                if len(skillTwoDescription) > 1024 and hasTwoSkills:
                    embedCharLimit = "(This character's skill description exceeds Discord's character limit. " \
                                     "Please see the wiki link below for the full description.)"
                    embed.add_field(name="Skill 2", value=embedCharLimit, inline=False)
                elif hasTwoSkills:
                    embed.add_field(name="Skill 2", value=skillTwoDescription, inline=False)

                embed.add_field(name="Abilities", value=abilities, inline=False)
                embed.add_field(name="Wiki Link",
                                value=f"[Click here](https://dragalialost.wiki/{formattedName})", inline=False)
                embed.add_field(name="Co-ability", value=entityDict["co_ability"], inline=True)
                embed.add_field(name="Chain Co-ability", value=entityDict["chain_co_ability"], inline=True)

                obtainMethod = "This adventurer is obtainable via " + entityDict["obtain_method"] + "."
                footerTip = "\nType ?commands to get a list of available commands."
                embed.set_footer(text=obtainMethod + footerTip)
                await ctx.send(file=icon, embed=embed)

            # entity is a dragon
            elif entityDict["type"] == DRAGON:
                name = entityDict["name"].replace(" ", "_")
                emojiString = info_methods.get_dragon_emojis(entityDict["rarity"], entityDict["element"])
                embed = discord.Embed(title=entityDict["name"], description=emojiString, color=0x3D85C6)
                print(name)
                icon = discord.File(f"./dragons/{name}.png", filename=f"{name}.png")
                # NOTE: currently issue with accented characters and special chars like &
                embed.set_thumbnail(url=f"attachment://{unidecode.unidecode(name)}.png")

                formattedName = name.replace(" ", "_")
                skillOneDescription = info_methods.print_skills(entityDict["skill_one"], entityDict["skill_one_desc"],
                                                                DRAGON)
                abilities = info_methods.print_abilities([entityDict["ability_one"], entityDict["ability_two"]])

                embed.add_field(name="Skill", value=skillOneDescription, inline=False)
                embed.add_field(name="Abilities", value=abilities, inline=False)
                embed.add_field(name="Wiki Link",
                                value=f"[Click here](https://dragalialost.wiki/{formattedName})", inline=False)
                embed.set_footer(text="Type ?commands to get a list of available commands.")
                await ctx.send(file=icon, embed=embed)
    else:
        await ctx.send(f"'{entity}' is not a valid name.")


@bot.command(aliases=["wyrmprint"])
async def wp(ctx, *, arg: str):
    """
    Retrieves information about wyrmprints that might have a requested ability
    and prints it to the Discord text channel.
    :param ctx: Context command was issued
    :param arg: String entered in by user containing search parameters
    :return:
    """
    name = arg

    if len(name) < 1:
        await ctx.send("Please enter a search parameter.")
    else:
        wyrmprint = wp_methods.make_dict(string.capwords(name))
        if wyrmprint is None:
            embedTitle = f"Search Result for: '{string.capwords(name)}'"
            embed = discord.Embed(title=embedTitle, color=0x3D85C6)
            description = "You may want to refine your search parameter. Please type the full name of the wyrmprint."
            embed.add_field(name="Nothing here...", value=description, inline=False)
        else:
            embed = discord.Embed(color=0x3D85C6)
            description = findwp_methods.pretty_print(wyrmprint)
            if wyrmprint["rarity"] == "5":
                wyrmprintName = emojis.RARITY_FIVE + findwp_methods.get_affinity_emoji(wyrmprint["affinity"]) + \
                                " " + wyrmprint["name"]
                embed.add_field(name=wyrmprintName, value=description, inline=False)
            if wyrmprint["rarity"] == "4":
                wyrmprintName = emojis.RARITY_FOUR + findwp_methods.get_affinity_emoji(wyrmprint["affinity"]) + \
                                " " + wyrmprint["name"]
                embed.add_field(name=wyrmprintName, value=description, inline=False)
            if wyrmprint["rarity"] == "3":
                wyrmprintName = emojis.RARITY_THREE + findwp_methods.get_affinity_emoji(wyrmprint["affinity"]) + \
                                " " + wyrmprint["name"]
                embed.add_field(name=wyrmprintName, value=description, inline=False)

    embed.set_footer(text="Type ?commands to get a list of available commands.")

    await ctx.send(embed=embed)


@bot.command(aliases=["findwyrmprint", "findwyrmprints"])
async def findwp(ctx, *, arg: str):
    """
    Retrieves information about wyrmprints that might have a requested ability
    and prints it to the Discord text channel.
    :param ctx: Context command was issued
    :param arg: String entered in by user containing search parameters
    :return:
    """
    ability = arg

    if len(ability) < 4:
        await ctx.send("Please enter a longer search parameter.")
    else:
        # get list of wyrmprints (dictionaries)
        wyrmprintList = findwp_methods.make_list(ability)
        embedTitle = f"Search Result for Wyrmprints Containing: '{ability}'"
        embed = discord.Embed(title=embedTitle, color=0x3D85C6)

        if len(wyrmprintList) == 0:
            description = "You may want to refine your search parameter."
            embed.add_field(name="Nothing here...", value=description, inline=False)
        else:
            for wyrmprint in wyrmprintList:
                description = findwp_methods.pretty_print(wyrmprint)
                if wyrmprint["rarity"] == "5":
                    wyrmprintName = emojis.RARITY_FIVE + findwp_methods.get_affinity_emoji(wyrmprint["affinity"]) + \
                           " " + wyrmprint["name"]
                    embed.add_field(name=wyrmprintName, value=description, inline=False)
                elif wyrmprint["rarity"] == "4":
                    wyrmprintName = emojis.RARITY_FOUR + findwp_methods.get_affinity_emoji(wyrmprint["affinity"]) + \
                           " " + wyrmprint["name"]
                    embed.add_field(name=wyrmprintName, value=description, inline=False)
                elif wyrmprint["rarity"] == "3":
                    wyrmprintName = emojis.RARITY_THREE + findwp_methods.get_affinity_emoji(wyrmprint["affinity"]) + \
                           " " + wyrmprint["name"]
                    embed.add_field(name=wyrmprintName, value=description, inline=False)

        embed.set_footer(text="Type ?commands to get a list of available commands.")
        await ctx.send(embed=embed)


@bot.command(aliases=["find_affinities"])
async def affinities(ctx):
    """
    Displays a list of affinities (wyrmprint set effects).
    :param ctx: Context command was issued
    :return: None
    """
    file = open("affinityList.txt", "r")
    await ctx.send(file.read())
    file.close()


@bot.command(aliases=["find_affinity"])
async def affinity(ctx, *, arg: str):
    """
    Retrieves a list of wyrmprints with the requested affinity.
    :param ctx: Context command was issued
    :param arg: String entered in by user containing search parameters
    :return:
    """
    ability = arg

    if len(ability) < 4:
        await ctx.send("Please enter a longer search parameter.")
    else:
        # get list of wyrmprints (dictionaries)
        wyrmprintList = findwp_methods.make_affinity_list(ability)
        embedTitle = f"Search Result for Wyrmprints Containing the Affinity: '{ability}'"
        embed = discord.Embed(title=embedTitle, color=0x3D85C6)

        if len(wyrmprintList) == 0:
            description = "You may want to fix your spelling of the affinity."
            embed.add_field(name="Nothing here...", value=description, inline=False)
        else:
            for wyrmprint in wyrmprintList:
                description = findwp_methods.pretty_print(wyrmprint)
                if wyrmprint["rarity"] == "5":
                    wyrmprintName = emojis.RARITY_FIVE + findwp_methods.get_affinity_emoji(wyrmprint["affinity"]) + \
                           " " + wyrmprint["name"]
                    embed.add_field(name=wyrmprintName, value=description, inline=False)
                elif wyrmprint["rarity"] == "4":
                    wyrmprintName = emojis.RARITY_FOUR + findwp_methods.get_affinity_emoji(wyrmprint["affinity"]) + \
                           " " + wyrmprint["name"]
                    embed.add_field(name=wyrmprintName, value=description, inline=False)
                elif wyrmprint["rarity"] == "3":
                    wyrmprintName = emojis.RARITY_THREE + findwp_methods.get_affinity_emoji(wyrmprint["affinity"]) + \
                           " " + wyrmprint["name"]
                    embed.add_field(name=wyrmprintName, value=description, inline=False)

        embed.set_footer(text="Type ?commands to get a list of available commands.")
        await ctx.send(embed=embed)


@bot.command(aliases=["manaspiral", "spirals"])
async def manaspirals(ctx):
    """
    Retrieves a list of adventurers who have obtained a mana spiral.
    :param ctx: Context command was issued
    :return:
    """
    adventurerList = manaspiral_methods.make_list()
    embedTitle = f"List of Adventurers with a Mana Spiral:"
    embed = discord.Embed(title=embedTitle, color=0x3D85C6)

    embed.add_field(name=emojis.RARITY_FIVE + " 5", value=manaspiral_methods.pretty_print(adventurerList, "5"), inline=False)
    embed.add_field(name=emojis.RARITY_FOUR + " 4", value=manaspiral_methods.pretty_print(adventurerList, "4"), inline=False)
    embed.add_field(name=emojis.RARITY_THREE + " 3", value=manaspiral_methods.pretty_print(adventurerList, "3"), inline=False)
    embed.set_footer(text="Type ?commands to get a list of available commands.")

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
