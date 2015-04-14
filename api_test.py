import unittest

from api import RiotAPI
from personal_data import *

class TestApiMethods(unittest.TestCase):

    def setUp(self):
        self.api = RiotAPI(my_key)
      
    def test_champion_id_from_name(self):
        self.assertEqual(self.api._get_champion_id("Thresh"), 412)
        
    def test_champion_name_from_id(self):
        self.assertEqual(self.api._get_champion_name(412), "Thresh")

    def test_summoner_id(self):
        self.assertEqual(self.api._get_id_by_summoner_name("Peng Yiliang"), 44979328)
        
    def test_ult_cooldwons_for_ori(self):
        self.assertEqual(self.api.get_ult_cooldowns("Orianna"), (120, 105, 90))
        
if __name__ == '__main__':
    unittest.main()