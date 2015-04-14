import requests

from RiotAPI_Interface.api import RiotAPI
import personal_data

class CooldownPrinter(RiotAPI):
    def get_ult_cooldowns_for_match(self, name):
        """Returns a list of pairs of champion name and ultimate cooldowns for current match"""
        allies, enemies = self.get_champions_in_match_by_team(name)
        get_cds  = lambda champions: [(champion, self.get_ult_cooldowns(champion))
                                        for champion in champions]
        return get_cds(allies), get_cds(enemies)
        
    def print_ult_cooldowns_for_match(self, name):
        allies, enemies = self.get_ult_cooldowns_for_match(name)
        print("Ally team:")
        self._print_ult_cooldowns(allies)
        print("\nEnemy team:")
        self._print_ult_cooldowns(enemies)

    def _print_ult_cooldowns(self, cd_info):        
        for line in cd_info:
            print("{champion}:  {cds}".format(champion=line[0], cds=line[1]))
            
            
def main():
    api_key = personal_data.my_key
    requests.packages.urllib3.disable_warnings()  #Suppresses Insecure Connection warnings
    cd_printer = CooldownPrinter(api_key)
    cd_printer.print_ult_cooldowns_for_match(personal_data.name)
    
if __name__ == "__main__":
    main()