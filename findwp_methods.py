import sqlite3


def make_list(parameters):
    """
    Retrieves table content and creates a list of dictionaries containing wyrmprint entries.
    :param parameters: string entered in by user containing search parameters
    :return: dict containing wyrmprint info
    """
    connection = sqlite3.connect("dragalia.db")
    connection.row_factory = sqlite3.Row
    cursorObj = connection.cursor()

    cursorObj.execute("SELECT * FROM Wyrmprints WHERE ability_one LIKE ? OR ability_two LIKE ? OR ability_three LIKE ?",
                      ("%" + parameters + "%", "%" + parameters + "%", "%" + parameters + "%",))
    result = [dict(row) for row in cursorObj.fetchall()]

    connection.close()

    return result


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
