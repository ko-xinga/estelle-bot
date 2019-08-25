import requests
from bs4 import BeautifulSoup


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
    # for each tr tag...
    for trTag in rawTable.find_all("tr"):
        # find all td tags (two exactly)
        tdTags = trTag.find_all("td")
        # first column = key; second = value
        entityDict[tdTags[0].string] = tdTags[1].string

    spanTag = soup.find("span", {"class": "mw-headline"})
    if "adventurer" in spanTag.text.lower():
        entityDict["entityType"] = "adventurer"
    elif "dragon" in spanTag.text.lower():
        entityDict["entityType"] = "dragon"

    return entityDict


def get_image(entityType, rarity, entityID, variation):
    """
    Retrieves thumbnail of entity
    :param entityType: string representing if the entity is an adventurer or dragon
    :param rarity: integer representing the rarity of the entity
    :param entityID: integer representing the ID of the entity
    :param variation: integer representing if the entity requested is an original or themed variation
    :return: url of the entity's thumbnail
    """
    if entityType == "adventurer":
        response = requests.get(f"https://dragalialost.gamepedia.com/File:{entityID}_0{variation}_r0{rarity}.png")
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", {"class": "fullImageLink"})
        link = div.find("a")["href"]
        return link

    elif entityType == "dragon":
        response = requests.get(f"https://dragalialost.gamepedia.com/File:{entityID}_0{variation}.png")
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", {"class": "fullImageLink"})
        link = div.find("a")["href"]
        return link


def get_skill(entityType, skillName, maxSkillLevel):
    """
    Retrieves skill description.
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

    rawTable = soup.find_all("tr")
    for trTag in rawTable:
        tdTags = trTag.find_all("td")
        if tdTags[0].string == "Description3" and tdTags[0].string == maxSkillLevel:
            skillDescription = tdTags[1].get_text()
        elif tdTags[0].string == "Description2" and tdTags[0].string == maxSkillLevel:
            skillDescription = tdTags[1].get_text()
        if tdTags[0].string == "Sp":
            skillCost = tdTags[1].get_text()
    if entityType == "adventurer":
        skillDescription = skillDescription + " [" + skillCost + " SP]"

    return skillDescription


def pretty_print(skillName, description):
    """
    Formats the skill and its description so they can be embedded into Discord
    :param skillName: string representing skill name
    :param description: string representing lengthy skill description
    :return: formatted string
    """
    return "**" + skillName + "** " + description
