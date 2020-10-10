import sqlite3
import emojis

def make_list(parameters):
    """
    Retrieves table content and creates a list of dictionaries containing wyrmprint entries.
    :param parameters: string entered in by user containing search parameters
    :return: dict containing wyrmprint info
    """
    connection = sqlite3.connect("dragalia.db")
    connection.row_factory = sqlite3.Row
    cursorObj = connection.cursor()

    cursorObj.execute("SELECT * FROM Wyrmprints WHERE ability_one LIKE ? OR ability_two LIKE ?",
                      ("%" + parameters + "%", "%" + parameters + "%",))
    result = [dict(row) for row in cursorObj.fetchall()]

    connection.close()

    return result


def make_affinity_list(parameters):
    """
    Retrieves table content and creates a list of dictionaries containing wyrmprint entries.
    :param parameters: string entered in by user containing search parameters
    :return: dict containing wyrmprint info
    """
    connection = sqlite3.connect("dragalia.db")
    connection.row_factory = sqlite3.Row
    cursorObj = connection.cursor()

    cursorObj.execute("SELECT * FROM Wyrmprints WHERE affinity LIKE ?",
                      ("%" + parameters + "%",))
    result = [dict(row) for row in cursorObj.fetchall()]

    connection.close()

    return result

def get_affinity_emoji(affinity):
    if affinity == "Bull's Boon":
        return emojis.BULLS_BOON
    elif affinity == "Lance's Boon":
        return emojis.LANCES_BOON
    elif affinity == "Wolf's Boon":
        return emojis.WOLFS_BOON
    elif affinity == "Sword's Boon":
        return emojis.SWORDS_BOON
    elif affinity == "Serpent's Boon":
        return emojis.SERPENTS_BOON
    elif affinity == "Eagle's Boon":
        return emojis.EAGLES_BOON
    elif affinity == "Axe's Boon":
        return emojis.AXES_BOON
    elif affinity == "Crown's Boon":
        return emojis.CROWNS_BOON
    elif affinity == "Bow's Boon":
        return emojis.BOWS_BOON
    elif affinity == "Staff's Boon":
        return emojis.STAFFS_BOON
    elif affinity == "Dragon's Boon":
        return emojis.DRAGONS_BOON
    # return blank if no affinity
    else:
        return ""


def get_affinity_effect(affinity):
    if affinity == "Bull's Boon":
        return "(Bull's Boon 2|2) Reduces susceptibility to paralysis by 100%."
    elif affinity == "Lance's Boon":
        return "(Lance's Boon 2|3|4) Increases force strike damage by 5|8|15%."
    elif affinity == "Wolf's Boon":
        return "(Wolf's Boon 2|2) Reduces susceptibility to stun by 100%."
    elif affinity == "Sword's Boon":
        return "(Sword's Boon 4|4) Increases strength by 8%."
    elif affinity == "Serpent's Boon":
        return "(Serpent's Boon 2|2) Reduces susceptibility to curses by 100%."
    elif affinity == "Eagle's Boon":
        return "(Eagle's Boon 2|2) Reduces susceptibility to burning by 100%."
    elif affinity == "Axe's Boon":
        return "(Axe's Boon 4|4) Increases damage to enemies in break state by 10%."
    elif affinity == "Crown's Boon":
        return "(Crown's Boon 4|4) Increases attack skill damage by 10%."
    elif affinity == "Bow's Boon":
        return "(Bow's Boon 3|4) Increases skill gauge fill rate by 6|10%."
    elif affinity == "Staff's Boon":
        return "(Staff's Boon 2|3|4) Increases duration of buff skills by 5|8|15%."
    elif affinity == "Dragon's Boon":
        return "(Dragon's Boon 2|3|4) Adds 10|18|30% to the modifier applied to damage when in dragon form."
    # return blank if no affinity
    else:
        return ""


def pretty_print(wyrmprintDict):
    """
    Formats the wyrmprint abilities so they can be embedded into Discord.
    :param wyrmprintDict: dict containing wyrmprint information
    :return: formatted string
    """
    prettyString = ""
    if wyrmprintDict is not None:
        if wyrmprintDict["ability_two"] != "":
            prettyString = wyrmprintDict["ability_one"] + "\n" + wyrmprintDict["ability_two"]
        else:
            prettyString = wyrmprintDict["ability_one"]
    else:
        return None

    if wyrmprintDict["affinity"] != "":
        prettyString = prettyString + "\n*" + get_affinity_effect(wyrmprintDict["affinity"]) + "*"

    return prettyString
