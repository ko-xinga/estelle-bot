import sqlite3


def make_dict(parameter):
    """
    Retrieves table content and creates a dictionary containing wyrmprint information.
    :param parameter: string entered in by user containing search parameters
    :return: dict containing wyrmprint info
    """
    connection = sqlite3.connect("dragalia.db")
    connection.row_factory = sqlite3.Row
    cursorObj = connection.cursor()

    cursorObj.execute("SELECT name FROM Wyrmprints WHERE name = ? COLLATE NOCASE", (parameter,))
    query = cursorObj.fetchone()

    # check if wyrmprint exists
    if query is None:
        connection.close()
        return None
    else:
        cursorObj.execute("SELECT * FROM Wyrmprints WHERE name= ? COLLATE NOCASE", (parameter,))
        result = [dict(row) for row in cursorObj.fetchall()]
        connection.close()
        wyrmprint = result[0]
        return wyrmprint


def pretty_print(wyrmprintDict):
    """
    Formats the wyrmprint abilities so they can be embedded into Discord.
    :param wyrmprintDict: dict containing wyrmprint information
    :return: formatted string
    """
    prettyString = ""
    if wyrmprintDict is not None:
        if wyrmprintDict["ability_two"] != "" and wyrmprintDict["ability_three"] != "":
            prettyString = wyrmprintDict["ability_one"] + "\n" + wyrmprintDict["ability_two"] + "\n" + \
                           wyrmprintDict["ability_three"]
        elif wyrmprintDict["ability_two"] != "":
            prettyString = wyrmprintDict["ability_one"] + "\n" + wyrmprintDict["ability_two"]
        else:
            prettyString = wyrmprintDict["ability_one"]
    else:
        return None

    return prettyString
