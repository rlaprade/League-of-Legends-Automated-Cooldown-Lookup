import unittest

from api import RiotAPI
from personal_data import *

class TestApiMethods(unittest.TestCase):

    def setUp(self):
        self.api = RiotAPI(my_key)
      
    def test_champion_id(self):
        self.assertEqual(self.api.get_champion_id("Thresh"), 412)

    def test_champion_id(self):
        self.assertEqual(self.api.get_id_by_summoner_name("Peng Yiliang"), 44979328)
        
if __name__ == '__main__':
    unittest.main()