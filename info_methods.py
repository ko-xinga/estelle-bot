import requests
from bs4 import BeautifulSoup

JUICY_MEAT = "1"
KALEIDOSCOPE = "2"
FLORAL_CIRCLET = "3"
COMPELLING_BOOK = "4"
MANA_ESSENCE = "5"


def make_dict(entityName):
    """
    Retrieves table content from entity page and puts it in a dict.
    :param entityName: string entered in by user containing entity name
    :return: dict containing entity info
    """
    response = requests.get(f"https://dragalialost.gamepedia.com/index.php?title={entityName.title()}&action=pagevalues")
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    rawTable = soup.find("table", {"class": "wikitable mw-page-info"})
    entityDict = {}
    # turn table containing entity info into a dictionary
    for trTag in rawTable.find_all("tr"):
        tdTags = trTag.find_all("td")
        entityDict[tdTags[0].string] = tdTags[1].string

    # determine if entity is an adventurer or dragon
    spanTag = soup.find("span", {"class": "mw-headline"})
    if "adventurer" in spanTag.text.lower():
        entityDict["entityType"] = "adventurer"
    elif "dragon" in spanTag.text.lower():
        entityDict["entityType"] = "dragon"

    return entityDict


def get_image(entityType, rarity, entityID, variation):
    """
    Retrieves thumbnail of entity.
    :param entityType: string representing if the entity is an adventurer or dragon
    :param rarity: integer representing the rarity of the entity
    :param entityID: integer representing the ID of the entity
    :param variation: integer representing if the entity requested is an original or themed variation
    :return: string containing url of the entity's thumbnail
    """
    if entityType == "adventurer":
        response = requests.get(f"https://dragalialost.gamepedia.com/File:{entityID}_0{variation}_r0{rarity}.png")
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", {"class": "fullImageLink"})
        link = div.find("a")["href"]
        return link

    elif entityType == "dragon":
        # dragons can't be promoted unlike adventurers
        response = requests.get(f"https://dragalialost.gamepedia.com/File:{entityID}_0{variation}.png")
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", {"class": "fullImageLink"})
        link = div.find("a")["href"]
        return link


def get_skill(entityType, skillName, maxSkillLevel):
    """
    Retrieves skill description.
    :param entityType: string representing if the entity is an adventurer or dragon
    :param skillName: string representing skill name
    :param maxSkillLevel: string representing highest level the skill can become
    :return: string containing the concatenated description
    """
    skillDescription = ""
    skillCost = ""
    urlPart = skillName.replace(" ", "_")
    response = requests.get(f"https://dragalialost.gamepedia.com/index.php?title={urlPart}&action=pagevalues")
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # look for columns containing the skill descriptions and extract them
    rawTable = soup.find_all("tr")
    for trTag in rawTable:
        tdTags = trTag.find_all("td")
        # if its the first skill, get the description from the Description3 field
        if tdTags[0].string == "Description3" and tdTags[0].string == maxSkillLevel:
            skillDescription = tdTags[1].get_text()
        # if its the second skill, get the description from the Description2 field
        elif tdTags[0].string == "Description2" and tdTags[0].string == maxSkillLevel:
            skillDescription = tdTags[1].get_text()
        if tdTags[0].string == "Sp":
            skillCost = tdTags[1].get_text()

    # concatenate SP cost to adventurer skills (dragons don't have SP values)
    if entityType == "adventurer":
        skillDescription = skillDescription.rstrip() + " [" + skillCost + " SP]"

    return skillDescription


def get_footer(entityDict):
    """
    Returns the concatenated footer containing misc. info.
    :param entityDict: dict containing entity info
    :return: concatenated string containing misc. info
    """
    if entityDict["entityType"] == "adventurer":
        return entityDict["Rarity"] + "* | " + entityDict["ElementalType"] + " | " + \
               entityDict["WeaponType"] + " | " + entityDict["CharaType"]
    elif entityDict["entityType"] == "dragon":
        return entityDict["Rarity"] + "* | " + entityDict["ElementalType"]


def get_favorite(gift):
    """
    Returns the dragon's favorite roost item.
    :param gift: string representing a value of which roost item is preferred by the dragon
    :return: string containing hard-coded value
    """
    if gift == JUICY_MEAT:
        return "Juicy Meat (Monday)"
    if gift == KALEIDOSCOPE:
        return "Kaleidoscope (Tuesday)"
    if gift == FLORAL_CIRCLET:
        return "Floral Circlet (Wednesday)"
    if gift == COMPELLING_BOOK:
        return "Compelling Book (Thursday)"
    if gift == MANA_ESSENCE:
        return "Mana Essence (Friday)"


def pretty_print(skillName, description):
    """
    Formats the skill and its description so they can be embedded into Discord.
    :param skillName: string representing skill name
    :param description: string representing lengthy skill description
    :return: formatted string
    """
    return "**" + skillName + "**: " + description
