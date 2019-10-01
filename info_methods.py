import sqlite3

ADVENTURER = "adventurer"
DRAGON = "dragon"

def make_dict(entityName):
    """
    Retrieves table content and puts it in a dict.
    :param entityName: string entered in by user containing entity name
    :return: dict containing entity info, otherwise return None
    """
    connection = sqlite3.connect("dragalia.db")
    connection.row_factory = sqlite3.Row
    cursorObj = connection.cursor()

    # check if the entity is an adventurer
    cursorObj.execute("SELECT name FROM Adventurers WHERE name = ?", (entityName,))
    query = cursorObj.fetchone()
    if query is None:
        # check if the entity is a dragon
        cursorObj.execute("SELECT name FROM Dragons WHERE name = ?", (entityName,))
        query = cursorObj.fetchone()
        if query is None:
            return None
        else:
            cursorObj.execute("SELECT * FROM Dragons WHERE name=?", (entityName,))
            result = [dict(row) for row in cursorObj.fetchall()]
            entityDict = result[0]
            entityDict["type"] = "dragon"
    else:
        cursorObj.execute("SELECT * FROM Adventurers WHERE name=?", (entityName,))
        result = [dict(row) for row in cursorObj.fetchall()]
        entityDict = result[0]
        entityDict["type"] = "adventurer"

    connection.close()

    return entityDict


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


def print_skills(skillName, description, type):
    """
    Formats the skill and its description so they can be embedded into Discord.
    :param skillName: string representing skill name
    :param description: string representing lengthy skill description
    :return: formatted string
    """
    prettyString = ""

    if type == ADVENTURER:
        prettyString = "**" + skillName + "**: " + description.replace("\n", "")
    elif type == DRAGON:
        prettyString = "**" + skillName + "**: " + description.replace("\n", "")
        # remove sp cost
        prettyString = prettyString.split(" [")
        prettyString = prettyString[0]

    return prettyString


def print_abilities(abilityList):
    """
    Formats the abilities so they can be embedded into Discord.
    :param abilityList: list containing all the abilities
    :return: formatted string
    """
    prettyString = ""

    for ability in abilityList:
        if ability != abilityList[-1]:
            prettyString = prettyString + ability + "\n"
        else:
            prettyString += ability

    return prettyString
