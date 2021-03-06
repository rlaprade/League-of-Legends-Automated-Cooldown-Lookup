import requests

from constants import *


class RiotAPI(object):
    def __init__(self, api_key, region=REGIONS["north_america"]):
        self.api_key = api_key
        self.region = region
        self.champ_list = self._champion_list()
        self.champ_data = self.champ_list["data"]
        self.name_map = self._champion_name_to_id_map()  # Maps champion name to id
        self.id_map = self._champion_id_to_name_map()    # Maps champion id to name
        
    def get_champions_in_match(self, name):
        """Returns a list of the champions in the current game with summoner of given name"""
        lst = []
        participant_data = self._current_match_participants(name)
        for p in participant_data:
            champion = self._get_champion_name(p["championId"])
            lst.append(str(champion))
        return lst
        
    def get_champions_in_match_by_team(self, name):
        """Returns two lists of the champions, one for each team,
        for the current game of the specified summoner (name)
        """
        allies = []
        enemies = []
        summoner_id = self._get_id_by_summoner_name(name)
        participant_data = self._current_match_participants(name)
        for p in participant_data:
            if p["summonerId"] == summoner_id:
                allies_id = p["teamId"]
        for p in participant_data:
            champion = self._get_champion_name(p["championId"])
            team_id = p["teamId"]
            if team_id == allies_id:
                allies.append(str(champion))
            else:
                enemies.append(str(champion))
        return allies, enemies
        
    def get_ult_cooldowns(self, champion):
        """Returns a tuple of the ultimate cooldown values for given champion"""
        ult = self._get_champion_ability_data(champion)[-1]
        return tuple(cd for cd in ult["cooldown"])
        
    # def get_ult_cooldowns_for_match(self, name):
        # """Returns a list of pairs of champion name and ultimate cooldowns for current match"""
        # allies, enemies = self.get_champions_in_match_by_team(name)
        # get_cds  = lambda champions: [(champion, self.get_ult_cooldowns(champion))
                                        # for champion in champions]
        # return get_cds(allies), get_cds(enemies)
        
    # def print_ult_cooldowns_for_match(self, name):
        # allies, enemies = self.get_ult_cooldowns_for_match(name)
        # print("Ally team:")
        # self._print_ult_cooldowns(allies)
        # print("\nEnemy team:")
        # self._print_ult_cooldowns(enemies)
        
    def _request(self, api_url, params={}):
        args = {'api_key':  self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        url = URL["base"].format(proxy=self.region, url=api_url)
        response = requests.get(url, params=args)
        return response.json()
        
    def _get_summoner_by_name(self, name):
        api_url = URL["summoner_by_name"].format(region=self.region,
                                                version=API_VERSIONS["summoner"], names=name)
        return self._request(api_url)
        
    def _get_id_by_summoner_name(self, name):    
        name = name.replace(" ", "").lower()
        return self._get_summoner_by_name(name)[name]["id"]
        
    def _get_champion_id(self, champion):
        return self.name_map[champion]
            
    def _get_champion_name(self, id):
        return self.id_map[id]
        
    def _get_champion_data(self, champion):
        id = self._get_champion_id(champion)
        api_url = URL["champion"].format(region=self.region, 
                                        version=API_VERSIONS["static-data"], id=id)
        return self._request(api_url)
        
    def _get_champion_ability_data(self, champion):
        """Returns a list of ability data objects (type dict)"""
        data = self._get_champion_data(champion)
        return data["spells"]

    def _champion_list(self):
        api_url = URL["champion_list"].format(region=self.region, 
                                            version=API_VERSIONS["static-data"])
        return self._request(api_url)
        
    def _champion_name_to_id_map(self):
        name_map = {}
        for c in self.champ_data.values():
            name_map[c["name"]] = c["id"]
        return name_map
        
    def _champion_id_to_name_map(self):
        id_map = {}
        for c in self.champ_data.values():
            id_map[c["id"]] = c["name"]
        return id_map
        
    def _current_match_by_id(self, id):
        """Returns current match data for given summoner id"""
        api_url = URL["curret_match"].format(platformId=PLATFORM_ID[self.region],
                                            summonerId=id)
        return self._request(api_url)
        
    def _current_match(self, name):
        """Returns current match data for given summoner name"""
        id = self._get_id_by_summoner_name(name)
        try:
            return self._current_match_by_id(id)
        except ValueError as e:
            if e.message == "No JSON object could be decoded":
                raise InputError("No match found for summoner {name}".format(name=name))
        
    def _current_match_participants(self, name):
        """Returns a list of participant data dicts 
        for the current match of specified summoner (name)
        """
        return self._current_match(name)["participants"]
        
    # def _print_ult_cooldowns(self, cd_info):        
        # for line in cd_info:
            # print("{champion}:  {cds}".format(champion=line[0], cds=line[1]))
            
class InputError(Exception):
    pass
        
