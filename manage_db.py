import sqlite3
import requests
import urllib.request as urlreq
import os
import unidecode
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

ADVENTURER_URL = "https://dragalialost.wiki/w/Adventurer_Detailed_List"
DRAGON_URL = "https://dragalialost.wiki/w/Dragon_List"
WYRMPRINT_URL = "https://dragalialost.wiki/w/Wyrmprint_List"
MAIN_URL = "https://dragalialost.wiki/w/Dragalia_Lost_Wiki"

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
    chain_co_ability TEXT,
    ability_one TEXT,
    ability_two TEXT,
    ability_three TEXT,
    release_date TEXT,
    obtain_method TEXT,
    mana_spiral TEXT
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

INITIALIZE_WYRMPRINTS_COMMAND = """
CREATE TABLE Wyrmprints (
    name TEXT PRIMARY KEY,
    rarity TEXT,
    affinity TEXT,
    ability_one TEXT,
    ability_two TEXT
);
"""

INITIALIZE_VOID_SCHEDULE_COMMAND = """
CREATE TABLE VoidSchedule (
    quest TEXT PRIMARY KEY,
    monday TEXT,
    tuesday TEXT,
    wednesday TEXT,
    thursday TEXT,
    friday TEXT,
    saturday TEXT,
    sunday TEXT
);
"""

INITIALIZE_MASTER_DRAGON_SCHEDULE_COMMAND = """
CREATE TABLE MasterDragonSchedule (
    quest TEXT PRIMARY KEY,
    monday TEXT,
    tuesday TEXT,
    wednesday TEXT,
    thursday TEXT,
    friday TEXT,
    saturday TEXT,
    sunday TEXT
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


def initialize_wyrmprints(cursorObj):
    """
    Creates Wyrmprints table.
    :param cursorObj: cursor pointing to sqlite database
    :return: error
    """
    try:
        cursorObj.execute(INITIALIZE_WYRMPRINTS_COMMAND)
    except sqlite3.OperationalError as error:
        print(f"From initialize_wyrmprints():\n\tDatabase Error: {error}")
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

        if None not in adventurerList and "None" not in adventurerList:
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

    # create a list containing all the information about the dragon
    for row in rawTable.find_all("tr"):
        columns = row.find_all("td")
        for column in columns:
            value = column.text.strip()
            dragonList.append(value)

            # get id of dragon, which is on the image at column 0
            if len(columns) != 0 and column == columns[0]:
                imageTag = column.find('img', alt=True)
                # check if image exists before attempting to scrape id
                try:
                    imageList = imageTag['alt'].split()
                except TypeError:
                    dragonList[0] = ""
                else:
                    # replace blank index with id
                    dragonList[0] = imageList[0] + "_" + imageList[1].replace(".png", "")

            # get the name of the first ability manually which is at column 7
            if len(columns) != 0 and column == columns[7]:
                title = column.find_all("a")
                try:
                    dragonList[7] = title[-1].text
                except IndexError:
                    dragonList[7] = ""

            # get the name of the second ability manually which is at column 8
            elif len(columns) != 0 and column == columns[8]:
                title = column.find_all("a")

                try:
                    # scrape weird formatting of wiki table
                    if len(title[-2].text) > 0:
                        dragonList[8] = title[-2].text
                    else:
                        dragonList[8] = title[-1].text
                except IndexError:
                    dragonList[8] = ""

        if None not in dragonList and "None" not in dragonList:
            insert_dragons(cursorObj, dragonList)
        dragonList = []


def update_wyrmprints(cursorObj):
    """
    Scrape wiki and update the Wyrmprints table.
    :param cursorObj: cursor pointing to sqlite database
    :return: none
    column 0 = icon, column 1 = name, column 2 = rarity, column 5 = affinity, column 6/7 = abilities
    """
    response = requests.get(WYRMPRINT_URL)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    rawTable = soup.find("table", {"class": "wikitable"})

    # expected size of 5: name, rarity, affinity, ability_one, ability_two
    wyrmprintList = []

    # create a list containing all the information about the wyrmprint
    for row in rawTable.find_all("tr"):
        columns = row.find_all("td")
        # skip empty td tags
        if len(columns) < 5:
            continue
        for column in columns:
            # get value at current column
            value = column.text.strip()

            # get the name of the wyrmprint and append it
            if len(columns) != 0 and column == columns[1]:
                wyrmprintList.append(value)

            # get the rarity of the wyrmprint
            if len(columns) != 0 and column == columns[2]:
                wyrmprintList.append(value)

            # get the affinity label if applicable
            if len(columns) != 0 and column == columns[5]:
                wyrmprintList.append(value)

            # get the name of the first ability manually
            if len(columns) != 0 and column == columns[-3]:
                title = column.find_all("a")
                try:
                    wyrmprintList.append(title[-1].text)
                except IndexError:
                    wyrmprintList.append("")

            # get the name of the second ability manually
            if len(columns) != 0 and column == columns[-2]:
                title = column.find_all("a")
                try:
                    wyrmprintList.append(title[-1].text)
                except IndexError:
                    wyrmprintList.append("")

        # populates table row by row
        if None not in wyrmprintList and "None" not in wyrmprintList:
            insert_wyrmprints(cursorObj, wyrmprintList)
        wyrmprintList = []


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
        name = unidecode.unidecode(name.replace(" ", "_"))
        # download picture if it doesn't already exist
        if not os.path.isfile(f"./adventurers/{name}.png"):
            try:
                response = requests.get(f"https://dragalialost.wiki/File:{idList[0]}_{idList[1]}_r0{rarity}.png")
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                div = soup.find("div", {"class": "fullImageLink"})
                link = div.find("a")["href"]
            except AttributeError:
                print(f"Error: Unable to download ID {idList[0]} variation {idList[1]}")
            else:
                urlreq.urlretrieve("https://dragalialost.wiki"+link, f"./adventurers/{name}.png")

    # retrieve all dragon images
    cursorObj.execute("SELECT id, name FROM Dragons")
    query = cursorObj.fetchall()
    for row in query:
        # split idVariation into id and entity variation
        (idVariation, name) = row
        idList = idVariation.split("_")
        name = unidecode.unidecode(name.replace(" ", "_"))
        # download picture if it doesn't already exist
        if not os.path.isfile(f"./dragons/{name}.png"):
            try:
                response = requests.get(f"https://dragalialost.wiki/File:{idList[0]}__{idList[1]}.png")
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                div = soup.find("div", {"class": "fullImageLink"})
                link = div.find("a")["href"]
            except AttributeError:
                print(f"Error: Unable to download ID {idList[0]} variation {idList[1]}")
            else:
                urlreq.urlretrieve("https://dragalialost.wiki"+link, f"./dragons/{name}.png")


def separate_skill_desc(skillBlock):
    """
    Separates the skill name and its description from the concatenated string.
    :param skillBlock: string containing all the skill info concatenated together
    :return: two strings (skill name and skill description)
    """
    skill = ""
    skillDesc = ""

    if len(skillBlock) > 0:
        if "Lv. 4:" in skillBlock:
            stringList = skillBlock.split("Lv. 4: ")
            skill = stringList[0]
            skillDesc = stringList[1]
            return skill, skillDesc
        elif "Lv. 3:" in skillBlock:
            stringList = skillBlock.split("Lv. 3: ")
            skill = stringList[0]
            skillDesc = stringList[1]
            return skill, skillDesc
        elif "Lv. 2:" in skillBlock:
            stringList = skillBlock.split("Lv. 2: ")
            skill = stringList[0]
            skillDesc = stringList[1]
            return skill, skillDesc
        elif "Lv. 1:" in skillBlock:
            stringList = skillBlock.split("Lv. 1: ")
            skill = stringList[0]
            skillDesc = stringList[1]
            return skill, skillDesc
    else:
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
                skill_two, skill_two_desc, co_ability, chain_co_ability, ability_one, 
                ability_two, ability_three, release_date, obtain_method, mana_spiral) 
            VALUES
                (?,?,?,?,?,
                ?,?,?,?,
                ?,?,?,?,?,
                ?,?,?,?,?);
    '''
    if len(row) != 0:
        try:
            if "Lv. 4:" in row[9]:
                manaSpiral = "yes"
            else:
                manaSpiral = "no"

            skillOne, skillOneDesc = separate_skill_desc(row[9])
            # check if adventurer only has one skill
            if row[10] == "-":
                skillTwo = row[10]
                skillTwoDesc = row[10]
            else:
                skillTwo, skillTwoDesc = separate_skill_desc(row[10])
            cursorObj.execute(sql, (row[0], unidecode.unidecode(row[1]), row[2], row[3], row[4],
                                    row[5], row[6], skillOne, skillOneDesc,
                                    skillTwo, skillTwoDesc, row[11].replace(" (Co-ability)", ""), row[12], row[13],
                                    row[14], row[15], row[17], row[18], manaSpiral,))
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
            cursorObj.execute(sql, (row[0], unidecode.unidecode(row[1]), row[2], row[3], skillOne,
                                    skillOneDesc, row[7], row[8], row[9],))
        except sqlite3.IntegrityError as error:
            print(f"From insert_dragons():\n\tDatabase Error: {error}")


def insert_wyrmprints(cursorObj, row):
    """
    Inserts wyrmprint info into table.
    :param cursorObj: cursor pointing to sqlite database
    :param row: list containing information about wyrmprint
    :return: none
    """
    sql = '''REPLACE INTO Wyrmprints
                    (name, rarity, affinity, ability_one, ability_two) 
                VALUES
                    (?,?,?,?,?);
        '''
    if len(row) != 0:
        try:
            # if wyrmprint has affinity
            if len(row) == 5:
                affinityName = row[2].split("\n")[0]
                cursorObj.execute(sql, (row[0], row[1], affinityName, row[3], row[4],))
            else:
                cursorObj.execute(sql, (row[0], row[1], "", row[2], row[3],))
        except sqlite3.IntegrityError as error:
            print(f"From insert_wyrmprints():\n\tDatabase Error: {error}")


def main():
    connection = sqlite3.connect("dragalia.db")
    cursorObj = connection.cursor()

    initialize_adventurers(cursorObj)
    initialize_dragons(cursorObj)
    initialize_wyrmprints(cursorObj)

    print("Now updating database...")
    update_adventurers(cursorObj)
    update_dragons(cursorObj)
    update_wyrmprints(cursorObj)

    print("Now downloading images...")
    download_images(cursorObj)

    print("Database is now up to date!")
    connection.commit()
    connection.close()


main()
