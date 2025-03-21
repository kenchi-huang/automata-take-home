import unittest
from Game import Game
from Scoreboard import Scoreboard
import pandas as pd

class Test(unittest.TestCase):
    def test_compute_logic(self):
        logic_dict = pd.read_json("rules.json").to_dict()
        game = Game()
        for p1_move in logic_dict:
            for p2_move in logic_dict:
                with self.subTest():
                    if p2_move in logic_dict[p1_move]["Defeats"]:
                        self.assertEqual(game.compute_logic(p1_move, p2_move), 1)
                    elif p1_move == p2_move:
                        self.assertEqual(game.compute_logic(p1_move, p2_move), 2)
                    else:
                        self.assertEqual(game.compute_logic(p1_move, p2_move), 0)

if __name__ == '__main__':
    unittest.main()