import requests

from personal_data import *

URL = {
    'base': "https://{proxy}.api.pvp.net/{url}",
    # api/lol
        "summoner_by_name":  "api/lol/{region}/v{version}/summoner/by-name/{names}",
        # Static Data
            "champion_list":  "api/lol/static-data/{region}/v{version}/champion",
            "champion":  "api/lol/static-data/{region}/v{version}/champion/{id}",
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

class RiotAPI(object):
    def __init__(self, api_key, region=REGIONS["north_america"]):
        self.api_key = api_key
        self.region = region
        self.champ_list = self._champion_list()
        self.name_map = self._champion_name_to_id_map()  # Maps champion name to id
        self.id_map = self._champion_id_to_name_map()    # Maps champion id to name
        
    def _request(self, api_url, params={}):
        args = {'api_key':  self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        response = requests.get(
                URL["base"].format(proxy=self.region, url=api_url), 
                params=args
            )
        return response.json()
        
    def get_summoner_by_name(self, name):
        api_url = URL["summoner_by_name"].format(region=self.region, version=API_VERSIONS["summoner"], names=name)
        return self._request(api_url)
        
    def get_id_by_summoner_name(self, name):    
        name = name.replace(" ", "").lower()
        return self.get_summoner_by_name(name)[name]["id"]
        
    def current_match(self, name):
        """Returns current match data for given summoner name"""
        id = self.get_id_by_summoner_name(name)
        return self._current_match(id)
        
    def get_champion_id(self, champion):
        # for champ in self.champ_list["data"]:
            # if champ["name"] == champion:
                # return champ["id"]
        # raise Exception("Champion not found")
        return self.name_map[champion]
        
    def _champion_list(self):
        api_url = URL["champion_list"].format(region=self.region, version=API_VERSIONS["static-data"])
        return self._request(api_url)
        
    def _champion_name_to_id_map(self):
        name_map = {}
        for c in self.champ_list["data"].values():
            name_map[c["name"]] = c["id"]
        return name_map
        
    def _champion_id_to_name_map(self):
        id_map = {}
        for c in self.champ_list["data"].values():
            id_map[c["id"]] = c["name"]
        return id_map
        
    def _current_match(self, id):
        """Returns current match data for given summoner id"""
        api_url = URL["curret_match"].format(platformId=PLATFORM_ID[self.region], summonerId=id)
        return self._request(api_url)
        
def main():
    api = RiotAPI(my_key)
    r = api.current_match("TSM Lustboy")
    # participants = r["participants"]
    # print(type(r["participants"][0]))
    # for p in participants:
        # print(p["teamId"])
    print(r)
    return r
    
if __name__ == "__main__":
    main()
        
