#!/usr/bin/python
import unittest

import monsters

class TestMonstersLibrary(unittest.TestCase):

    def test_basic_team_search(self):
        e = monsters.Team([monsters.F5(), monsters.A5()])
        t = monsters.compose_team(enemy=e, cost_limit=17800, max_length=6,
                return_first_winner=False)
        self.assertEqual(len(t), 4)
        self.assertIsInstance(t[0], monsters.W3)
        self.assertIsInstance(t[1], monsters.A1)
        self.assertIsInstance(t[2], monsters.E3)
        self.assertIsInstance(t[3], monsters.E1)
        pass

    def test_repeating_monsters(self):
        e = monsters.Team([monsters.W5()])
        t = monsters.compose_team(enemy=e, cost_limit=4200, max_length=6,
                return_first_winner=False)
        self.assertEqual(len(t), 4)
        self.assertIsInstance(t[0], monsters.A1)
        self.assertIsInstance(t[1], monsters.A1)
        self.assertIsInstance(t[2], monsters.A1)
        self.assertIsInstance(t[3], monsters.A1)
        pass

if __name__ == '__main__':
    unittest.main()
