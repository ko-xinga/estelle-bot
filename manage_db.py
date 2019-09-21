import sqlite3
import requests
import urllib.request as urlreq
import os
from bs4 import BeautifulSoup

ADVENTURER_URL = "https://dragalialost.gamepedia.com/Adventurer_Detailed_List"
DRAGON_URL = "https://dragalialost.gamepedia.com/Dragon_List"

ADVENTURER = "adventurer"
DRAGON = "dragon"

ATTACK = "Attack"
DEFENSE = "Defense"
SUPPORT = "Support"
HEALING = "Healing"

INITIALIZE_ADVENTURERS_COMMAND = """
CREATE TABLE Adventurers (
    id TEXT,
    name TEXT PRIMARY KEY,
    title TEXT,
    class TEXT,
    rarity TEXT,
    element TEXT,
    weapon TEXT,
    skill_one TEXT,
    skill_one_desc TEXT,
    skill_two TEXT,
    skill_two_desc TEXT,
    co_ability TEXT,
    ability_one TEXT,
    ability_two TEXT,
    ability_three TEXT,
    release_date TEXT,
    obtain_method TEXT
);
"""

INITIALIZE_DRAGONS_COMMAND = """
CREATE TABLE Dragons (
    id TEXT,
    name TEXT PRIMARY KEY,
    rarity TEXT,
    element TEXT,
    skill_one TEXT,
    skill_one_desc TEXT,
    ability_one TEXT,
    ability_two TEXT,
    release_date TEXT
);
"""


def initialize_adventurers(cursorObj):
    """
    Creates Adventurers table.
    :param cursorObj: cursor pointing to sqlite database
    :return: error
    """
    try:
        cursorObj.execute(INITIALIZE_ADVENTURERS_COMMAND)
    except sqlite3.OperationalError as error:
        print(f"From initialize_adventurers():\n\tDatabase Error: {error}")
        return error


def initialize_dragons(cursorObj):
    """
    Creates Dragons table.
    :param cursorObj: cursor pointing to sqlite database
    :return: error
    """
    try:
        cursorObj.execute(INITIALIZE_DRAGONS_COMMAND)
    except sqlite3.OperationalError as error:
        print(f"From initialize_dragons():\n\tDatabase Error: {error}")
        return error


def update_adventurers(cursorObj):
    """
    Scrape wiki and update the Adventurers table.
    :param cursorObj: cursor pointing to sqlite database
    :return: none
    """
    response = requests.get(ADVENTURER_URL)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    rawTable = soup.find("table", {"class": "wikitable"})

    adventurerList = []

    # create a list containing all the information about the adventurer
    for row in rawTable.find_all("tr"):
        columns = row.find_all("td")
        for column in columns:
            value = column.text.strip()
            adventurerList.append(value)

            # get id of adventurer
            if len(columns) != 0 and column == columns[0]:
                imageTag = column.find('img', alt=True)
                imageList = imageTag['alt'].split()
                # replace blank index with id
                adventurerList[0] = imageList[0] + "_" + imageList[1].replace(".png", "")

            # class column is just an image, so manually fill it in
            images = column.findAll("img", {})
            for image in images:
                if "Icon Type Row" in image["alt"]:
                    adventurerList[3] = get_adventurer_class(image["alt"])

        insert_adventurers(cursorObj, adventurerList)
        adventurerList = []


def update_dragons(cursorObj):
    """
    Scrape wiki and update the Dragons table.
    :param cursorObj: cursor pointing to sqlite database
    :return: none
    """
    response = requests.get(DRAGON_URL)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    rawTable = soup.find("table", {"class": "wikitable"})

    dragonList = []

    # create a list containing all the information about the adventurer
    for row in rawTable.find_all("tr"):
        columns = row.find_all("td")
        for column in columns:
            value = column.text.strip()
            dragonList.append(value)

            # get id of dragon
            if len(columns) != 0 and column == columns[0]:
                imageTag = column.find('img', alt=True)
                imageList = imageTag['alt'].split()
                # replace blank index with id
                dragonList[0] = imageList[0] + "_" + imageList[1].replace(".png", "")

            # get the name of the first ability manually
            if len(columns) != 0 and column == columns[-3]:
                title = column.find_all("a")
                try:
                    dragonList[7] = title[-1].text
                except IndexError:
                    dragonList[7] = ""
            # get the name of the second ability manually
            elif len(columns) != 0 and column == columns[-2]:
                title = column.find_all("a")
                try:
                    dragonList[8] = title[-1].text
                except IndexError:
                    dragonList[8] = ""

        insert_dragons(cursorObj, dragonList)
        dragonList = []


def download_images(cursorObj):
    """
    Downloads the icons of all the adventurers and dragons and stores them locally.
    :param cursorObj: cursor pointing to sqlite database
    :return: none
    """
    if not os.path.isdir("./adventurers"):
        os.mkdir("./adventurers")
    if not os.path.isdir("./dragons"):
        os.mkdir("./dragons")

    # retrieve all adventurer images
    cursorObj.execute("SELECT id, name, rarity FROM Adventurers")
    query = cursorObj.fetchall()
    for row in query:
        # split idVariation into id and entity variation
        (idVariation, name, rarity) = row
        idList = idVariation.split("_")
        name = name.replace(" ", "_")
        # download picture if it doesn't already exist
        if not os.path.isfile(f"./adventurers/{name}.png"):
            try:
                response = requests.get(f"https://dragalialost.gamepedia.com/File:{idList[0]}_{idList[1]}_r0{rarity}.png")
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                div = soup.find("div", {"class": "fullImageLink"})
                link = div.find("a")["href"]
            except AttributeError:
                print(f"Error: Unable to download ID {idList[0]} variation {idList[1]}")
            else:
                print(f"Downloading {name}'s image...")
                urlreq.urlretrieve(link, f"./adventurers/{name}.png")

    # retrieve all dragon images
    cursorObj.execute("SELECT id, name FROM Dragons")
    query = cursorObj.fetchall()
    for row in query:
        # split idVariation into id and entity variation
        (idVariation, name) = row
        idList = idVariation.split("_")
        name = name.replace(" ", "_")
        # download picture if it doesn't already exist
        if not os.path.isfile(f"./dragons/{name}.png"):
            try:
                response = requests.get(f"https://dragalialost.gamepedia.com/File:{idList[0]}__{idList[1]}.png")
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                div = soup.find("div", {"class": "fullImageLink"})
                link = div.find("a")["href"]
            except AttributeError:
                print(f"Error: Unable to download ID {idList[0]} variation {idList[1]}")
            else:
                print(f"Downloading {name}'s image...")
                urlreq.urlretrieve(link, f"./dragons/{name}.png")


def separate_skill_desc(skillBlock):
    """
    Separates the skill name and its description from the concatenated string.
    :param skillBlock: string containing all the skill info concatenated together
    :return: two strings (skill name and skill description)
    """
    # split skill description until we get the final level of the skill
    stringListOne = skillBlock.split("Lv. 1: ")
    stringListTwo = stringListOne[1].split("Lv. 2:")
    stringListThree = stringListTwo[1].split("Lv. 3:")

    skill = stringListOne[0].strip()
    skillDesc = stringListThree[-1].strip()

    return skill, skillDesc


def get_adventurer_class(tag):
    """
    Returns the appropriate adventurer class based on the tag contents.
    :param tag: string containing html tag text
    :return: string containing adventurer class type
    """
    if ATTACK in tag:
        return ATTACK
    if DEFENSE in tag:
        return DEFENSE
    if SUPPORT in tag:
        return SUPPORT
    if HEALING in tag:
        return HEALING


def insert_adventurers(cursorObj, row):
    """
    Inserts adventurer info into table.
    :param cursorObj: cursor pointing to sqlite database
    :param row: list containing information about adventurer
    :return: none
    """
    sql = '''REPLACE INTO Adventurers
                (id, name, title, class, rarity, 
                element, weapon, skill_one, skill_one_desc, 
                skill_two, skill_two_desc, co_ability, ability_one, 
                ability_two, ability_three, release_date, obtain_method) 
            VALUES
                (?,?,?,?,?,
                ?,?,?,?,
                ?,?,?,?,
                ?,?,?,?);
    '''
    if len(row) != 0:
        try:
            skillOne, skillOneDesc = separate_skill_desc(row[9])
            skillTwo, skillTwoDesc = separate_skill_desc(row[10])
            cursorObj.execute(sql, (row[0], row[1], row[2], row[3], row[4],
                                    row[5], row[6], skillOne, skillOneDesc,
                                    skillTwo, skillTwoDesc, row[11].replace(" (Co-ability)", ""), row[12],
                                    row[13], row[14], row[16], row[17],))
        except sqlite3.IntegrityError as error:
            print(f"From insert_adventurers():\n\tDatabase Error: {error}")


def insert_dragons(cursorObj, row):
    """
    Inserts dragon info into table.
    :param cursorObj: cursor pointing to sqlite database
    :param row: list containing information about dragon
    :return: none
    """
    sql = '''REPLACE INTO Dragons
                    (id, name, rarity, element, skill_one,
                    skill_one_desc, ability_one, ability_two, release_date) 
                VALUES
                    (?,?,?,?,?,
                    ?,?,?,?);
        '''
    if len(row) != 0:
        try:
            skillOne, skillOneDesc = separate_skill_desc(row[6])
            cursorObj.execute(sql, (row[0], row[1], row[2], row[3], skillOne,
                                    skillOneDesc, row[7], row[8], row[9],))
        except sqlite3.IntegrityError as error:
            print(f"From insert_dragons():\n\tDatabase Error: {error}")


def main():
    connection = sqlite3.connect("dragalia.db")
    cursorObj = connection.cursor()

    initialize_adventurers(cursorObj)
    initialize_dragons(cursorObj)

    print("Now updating database...")
    update_adventurers(cursorObj)
    update_dragons(cursorObj)

    print("Now downloading images...")
    download_images(cursorObj)

    print("Database is now up to date!")
    connection.commit()
    connection.close()


main()
