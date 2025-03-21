import pandas as pd
import datetime
from Scoreboard import Scoreboard
import pathlib

class SaveUtils:
    def __init__(self):
        pass

    def create_save(self, save_name, player1_name, player2_name, scoreboard, enable_computer):
        save = {
            "player1": player1_name,
            "player2": player2_name,
            "p1_score": scoreboard.get_p1_score(),
            "p2_score": scoreboard.get_p2_score(),
            "round": scoreboard.get_round(),
            "enable_computer": enable_computer
        }
        save_df = pd.DataFrame.from_dict(save, orient="index").transpose()
        save_df.to_csv("./Saves/" + save_name.replace(" ", "_") + ".csv", index=False)

    def delete_save(self, save_name):
        pathlib.Path.unlink("./Saves/" + save_name + ".csv")
    
    def overwrite_save(self, save_name, player1_name, player2_name, scoreboard, enable_computer):
        self.delete_save(save_name)
        self.create_save(save_name, player1_name, player2_name, scoreboard, enable_computer)

    def get_saves(self):
        saves = []
        for file in pathlib.Path(r"./Saves/").glob("*.csv"):
            saves.append(file.name[:-4])
        return saves
    
    def get_save(self, save_name):
        try:
            save_df = pd.read_csv("./Saves/" + save_name + ".csv", index_col=False).transpose()
            save_dict = save_df.to_dict(orient="index")
            for key in save_dict.keys():
                save_dict[key] = save_dict[key][0]
            return save_dict
        except:
            raise Exception("Save not found")
