import requests
import json
import argparse
from thefuzz import fuzz, process
from datetime import datetime, date

class Game:
    def __init__(self, name, desc, releaseDate, genres, developers, publishers, platforms, iconURL):
        self.name = name
        self.desc = desc
        self.releaseDate = releaseDate
        self.genres = genres
        self.developers = developers
        self.publishers = publishers
        self.platforms = platforms
        self.iconURL = iconURL

    def __str__(self):
        return f"{self.name}, {self.desc}, {self.releaseDate}, {self.genres}, {self.developers}, {self.publishers}, {self.platforms}, {self.iconURL}"

    def getJson(self):
        gameDict = {}
        gameDict["name"] = self.name
        gameDict["description"] = self.desc
        gameDict["releaseDate"] = self.releaseDate.isoformat()
        gameDict["genres"] = self.genres
        gameDict["developers"] = self.developers
        gameDict["publishers"] = self.publishers
        gameDict["platforms"] = self.platforms
        gameDict["iconURL"] = self.iconURL
        return json.dumps(gameDict,indent=2)


steamApiUrl = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"
steamGameDetailsUrl = "http://store.steampowered.com/api/appdetails?appids={0}"

def getGameList() -> dict:
    req = requests.get(steamApiUrl)

    if(req.status_code != 200):
        raise Exception(f"Unable to obtain game list, API returned status code {req.status_code}")

    return req.json()["applist"]["apps"]

def searchGameList(searchTerm: str, gameList: list[dict]) -> dict:
    for game in gameList:
        game['ratio'] = fuzz.ratio(searchTerm, game['name'])

    return(sorted(gameList, key=lambda d: d['ratio'], reverse=True))


def steamJsonFormatter(steamJson: dict) -> Game:

    name = steamJson["name"]
    description = steamJson["short_description"]

    release_date_string = steamJson["release_date"]["date"]
    release_date = datetime.strptime(release_date_string, "%d %b, %Y").date()

    iconURL = steamJson["header_image"]

    genres = []
    for genre in steamJson["genres"]:
        genres.append(genre["description"])

    developers = []
    for developer in steamJson["developers"]:
        developers.append(developer)

    publishers = []
    for publisher in steamJson["publishers"]:
        publishers.append(publisher)

    platforms = []
    for platform in steamJson["platforms"]:
        platforms.append(platform)

    game = Game(name,description,release_date,genres,developers,publishers,platforms,iconURL)

    return(game)

def getGameInfo(appId: str):
    req = requests.get(steamGameDetailsUrl.format(appId))

    steamJson = req.json()[str(appId)]
    if(steamJson["success"] == True):
        return steamJsonFormatter(steamJson["data"])
    else:
        raise Exception(f"Unable to get data for app id {appid}.")
        sys.exit(-1)




def setupArgs():
    parser = argparse.ArgumentParser(
        prog="GamePile API Helper",
        description="A tool written in python to obtain game information from SteamAPI."
        )
    parser.add_argument('searchterm',help="The game to search for.")
    parser.add_argument('-i','--index',type=int,default=0,help="The search result to fetch. Indexes from 0.")

    return(parser.parse_args())

if __name__ == "__main__":
    args = setupArgs()
    gameList = getGameList()

    games = searchGameList(args.searchterm, gameList)

    print(getGameInfo(games[args.index]["appid"]).getJson())

