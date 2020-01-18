import sqlite3


def make_list():
    """
    Retrieves table content and creates a list of dictionaries containing adventurers with mana spirals.
    :param
    :return: dict containing adventurers with spirals
    """
    connection = sqlite3.connect("dragalia.db")
    connection.row_factory = sqlite3.Row
    cursorObj = connection.cursor()

    cursorObj.execute("SELECT name, rarity FROM Adventurers WHERE mana_spiral LIKE ?",
                      ("%" + "yes" + "%",))
    # format is: {'name': 'Cassandra', 'rarity': '5'}
    result = [dict(row) for row in cursorObj.fetchall()]

    connection.close()

    return result


def pretty_print(adventurerDict, rarity):
    """
    Formats the adventurer (who all have mana spirals) names so they can be embedded into Discord.
    :param adventurerDict: dict containing all adventurers that have a mana spiral
    :param rarity: string representing rarity of adventurer
    :return: formatted string
    """
    prettyString = ""
    if adventurerDict is not None:
        for adventurer in adventurerDict:
            if adventurer != adventurerDict[-1] and adventurer["rarity"] == rarity:
                prettyString = prettyString + adventurer["name"] + "\n"
            elif adventurer["rarity"] == rarity:
                prettyString = prettyString + adventurer["name"]
    else:
        return None

    return prettyString
