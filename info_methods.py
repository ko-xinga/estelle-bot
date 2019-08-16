import requests
from bs4 import BeautifulSoup


def retrieve_dict(entity):
    """
    Retrieves table content from entity page and puts it in a dict
    :param entity: String entered in by user containing entity name
    :return: adventurerDict, dict containing entity info
    """
    # retrieve data from website
    response = requests.get(f"https://dragalialost.gamepedia.com/index.php?title={entity}&action=pagevalues")
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    rawTable = soup.find("table", {"class": "wikitable mw-page-info"})

    adventurerDict = {}
    # for each tr tag...
    for trTag in rawTable.findAll("tr"):
        # find all td tags (two exactly)
        tdTags = trTag.findAll("td")
        # first column = key; second = value
        adventurerDict[tdTags[0].string] = tdTags[1].string

    return adventurerDict
