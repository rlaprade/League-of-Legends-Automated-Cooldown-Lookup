URL = {
    'base': "https://{proxy}.api.pvp.net/{url}",
    # api/lol
        "summoner_by_name":  "api/lol/{region}/v{version}/summoner/by-name/{names}",
        # Static Data
            "champion_list":  "api/lol/static-data/{region}/v{version}/champion",
            "champion":  "api/lol/static-data/{region}/v{version}/champion/{id}?champData=all",
    # observer-mode
    "curret_match":  "observer-mode/rest/consumer/getSpectatorGameInfo/{platformId}/{summonerId}",
}

API_VERSIONS = {
    "summoner": "1.4",
    "static-data":  "1.2",
}

REGIONS = {
    "north_america": "na",
}

PLATFORM_ID = {
    "na":  "NA1",
}