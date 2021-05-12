import sqlite3

MONDAY = "monday"
TUESDAY = "tuesday"
WEDNESDAY = "wednesday"
THURSDAY = "thursday"
FRIDAY = "friday"
SATURDAY = "saturday"
SUNDAY = "sunday"


def make_void_list(dayNumber):
    """
    Retrieves table content and creates a list of dictionaries containing void battle double drop availability.
    :param
    :return: dict containing adventurers with spirals
    """
    connection = sqlite3.connect("dragalia.db")
    connection.row_factory = sqlite3.Row
    cursorObj = connection.cursor()

    day = ""
    if dayNumber == 0:
        day = MONDAY
    elif dayNumber == 1:
        day = TUESDAY
    elif dayNumber == 2:
        day = WEDNESDAY
    elif dayNumber == 3:
        day = THURSDAY
    elif dayNumber == 4:
        day = FRIDAY
    elif dayNumber == 5:
        day = SATURDAY
    elif dayNumber == 6:
        day = SUNDAY

    cursorObj.execute("SELECT * FROM VoidSchedule")
    result = [dict(row) for row in cursorObj.fetchall()]

    dayList = list(filter(lambda resultLambda: resultLambda[day] == "x2", result))
    filteredList = [sub["quest"] for sub in dayList]

    connection.close()
    return filteredList


def make_master_dragon_list(dayNumber):
    """
    Retrieves table content and creates a list of dictionaries containing master dragon availability.
    :param
    :return: dict containing adventurers with spirals
    """
    connection = sqlite3.connect("dragalia.db")
    connection.row_factory = sqlite3.Row
    cursorObj = connection.cursor()

    day = ""
    if dayNumber == 0:
        day = MONDAY
    elif dayNumber == 1:
        day = TUESDAY
    elif dayNumber == 2:
        day = WEDNESDAY
    elif dayNumber == 3:
        day = THURSDAY
    elif dayNumber == 4:
        day = FRIDAY
    elif dayNumber == 5:
        day = SATURDAY
    elif dayNumber == 6:
        day = SUNDAY

    cursorObj.execute("SELECT * FROM MasterDragonSchedule")
    result = [dict(row) for row in cursorObj.fetchall()]

    dayList = list(filter(lambda resultLambda: resultLambda[day] == "yes", result))
    filteredList = [sub["quest"] for sub in dayList]

    connection.close()
    return filteredList


def pretty_print(questList):
    """
    Formats the list of quests so they can be embedded into Discord.
    :param questList: dict containing all adventurers that have a mana spiral
    :return: formatted string
    """
    prettyString = ""
    if questList is not None:
        for quest in questList:
            if quest != questList[-1]:
                prettyString = prettyString + quest + "\n"
            else:
                prettyString = prettyString + quest
    else:
        return None

    return prettyString