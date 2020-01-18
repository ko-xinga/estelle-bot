import sqlite3

ADVENTURER = "adventurer"
DRAGON = "dragon"

# replace emoji ID's below; to get the emoji id, put a \ in front of the emoji in discord chat and press enter
RARITY_FIVE = "<:rar_5:630906532179214338>"
RARITY_FOUR = "<:rar_4:630906532187340810>"
RARITY_THREE = "<:rar_3:630906532199923722>"

ELEMENT_FLAME = "<:ele_flame:630911804591177758>"
ELEMENT_WIND = "<:ele_wind:630906532296392704>"
ELEMENT_WATER = "<:ele_water:630906531902390278>"
ELEMENT_LIGHT = "<:ele_light:630906531763847169>"
ELEMENT_SHADOW = "<:ele_shadow:630906531956785153>"

WEAPON_SWORD = "<:wep_sword:630906532271357972>"
WEAPON_BLADE = "<:wep_blade:630906532271357953>"
WEAPON_DAGGER = "<:wep_dagger:630906532275683388>"
WEAPON_AXE = "<:wep_axe:630906534309658654>"
WEAPON_LANCE = "<:wep_lance:630906532279877664>"
WEAPON_BOW = "<:wep_bow:630906532292460575>"
WEAPON_WAND = "<:wep_wand:630906532288266240>"
WEAPON_STAFF = "<:wep_staff:630906532271226880>"

CLASS_ATTACK = "<:class_attack:630906532191535134>"
CLASS_DEFENSE = "<:class_defense:630906532233740298>"
CLASS_SUPPORT = "<:class_support:630906532242128907>"
CLASS_HEALING = "<:class_healing:630906532321689600>"

MANA_SPIRAL = "<:mana_spiral:667919282310479894>"


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
            # get dict
            entityDict = result[0]
            entityDict["type"] = "dragon"
    else:
        cursorObj.execute("SELECT * FROM Adventurers WHERE name=?", (entityName,))
        result = [dict(row) for row in cursorObj.fetchall()]
        entityDict = result[0]
        entityDict["type"] = "adventurer"

    connection.close()

    return entityDict


def find_alternatives(entityName):
    """
    Find possible adventurers or dragons if the original entry cannot be found.
    :param entityName: string entered in by user containing entity name
    :return: list containing all possible entities
    """
    possibleList = []
    connection = sqlite3.connect("dragalia.db")
    cursorObj = connection.cursor()
    cursorObj.execute("SELECT name FROM Adventurers")
    adventurerList = [job[0] for job in cursorObj.execute("SELECT name FROM Adventurers")]
    cursorObj.execute("SELECT name FROM Dragons")
    dragonList = [job[0] for job in cursorObj.execute("SELECT name FROM Dragons")]

    # clear up common naming error
    if entityName == "Gala Euden":
        possibleList.append("Gala Prince")
    # look for possible names
    if len(entityName) > 1:
        for adventurerName in adventurerList:
            if entityName in adventurerName:
                possibleList.append(adventurerName)
        for dragonName in dragonList:
            if entityName in dragonName:
                possibleList.append(dragonName)

    connection.close()

    return possibleList


def get_adv_emojis(rarity, element, weapon, advClass, manaSpiral):
    """
    Return emoji ID of rarity, element, weapon, and class icons for the adventurer embed.
    :param rarity: string representing entity rarity
    :param element: string representing entity element
    :param weapon: string representing entity weapon
    :param advClass: string representing entity class
    :return: formatted string
    """
    rarityEmoji = ""
    elementEmoji = ""
    weaponEmoji = ""
    classEmoji = ""
    spiralEmoji = ""

    if rarity == "5":
        rarityEmoji = RARITY_FIVE
    elif rarity == "4":
        rarityEmoji = RARITY_FOUR
    elif rarity == "3":
        rarityEmoji = RARITY_THREE

    if element == "Flame":
        elementEmoji = ELEMENT_FLAME
    elif element == "Wind":
        elementEmoji = ELEMENT_WIND
    elif element == "Water":
        elementEmoji = ELEMENT_WATER
    elif element == "Light":
        elementEmoji = ELEMENT_LIGHT
    elif element == "Shadow":
        elementEmoji = ELEMENT_SHADOW

    if weapon == "Sword":
        weaponEmoji = WEAPON_SWORD
    elif weapon == "Blade":
        weaponEmoji = WEAPON_BLADE
    elif weapon == "Dagger":
        weaponEmoji = WEAPON_DAGGER
    elif weapon == "Axe":
        weaponEmoji = WEAPON_AXE
    elif weapon == "Lance":
        weaponEmoji = WEAPON_LANCE
    elif weapon == "Bow":
        weaponEmoji = WEAPON_BOW
    elif weapon == "Wand":
        weaponEmoji = WEAPON_WAND
    if weapon == "Staff":
        weaponEmoji = WEAPON_STAFF

    if advClass == "Attack":
        classEmoji = CLASS_ATTACK
    elif advClass == "Defense":
        classEmoji = CLASS_DEFENSE
    elif advClass == "Support":
        classEmoji = CLASS_SUPPORT
    elif advClass == "Healing":
        classEmoji = CLASS_HEALING

    if manaSpiral == "yes":
        spiralEmoji = MANA_SPIRAL

    prettyString = rarityEmoji + elementEmoji + weaponEmoji + classEmoji + spiralEmoji

    return prettyString


def get_dragon_emojis(rarity, element):
    """
    Return emoji ID of rarity and element icons for the dragon embed.
    :param rarity: string representing entity rarity
    :param element: string representing entity element
    :return: formatted string
    """
    rarityEmoji = ""
    elementEmoji = ""

    if rarity == "5":
        rarityEmoji = RARITY_FIVE
    elif rarity == "4":
        rarityEmoji = RARITY_FOUR
    elif rarity == "3":
        rarityEmoji = RARITY_THREE

    if element == "Flame":
        elementEmoji = ELEMENT_FLAME
    elif element == "Wind":
        elementEmoji = ELEMENT_WIND
    elif element == "Water":
        elementEmoji = ELEMENT_WATER
    elif element == "Light":
        elementEmoji = ELEMENT_LIGHT
    elif element == "Shadow":
        elementEmoji = ELEMENT_SHADOW

    prettyString = rarityEmoji + elementEmoji

    return prettyString


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


def print_alternatives(nameList):
    """
    Formats the possible names so they can be embedded into Discord.
    :param nameList: list containing all the names
    :return: formatted string
    """
    prettyString = ""
    if len(nameList) != 0:
        prettyString = "\nDid you mean...\n"
        for name in nameList:
            if name != nameList[-1]:
                prettyString = prettyString + "- " + name + "\n"
            else:
                prettyString = prettyString + "- " + name
        return prettyString
    else:
        return prettyString
