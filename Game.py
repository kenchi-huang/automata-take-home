import time
import os
import pandas as pd
from Scoreboard import Scoreboard
import random
from termcolor import colored
from Utils.InputUtils import InputUtils
from Utils.PrintUtils import PrintUtils
from Utils.SaveUtils import SaveUtils

class Game:
    def __init__(self, scoreboard = Scoreboard(), restart = False, player1_name = "", player2_name = "", enable_computer = True):
        self.restart = restart
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.logic_dict = pd.read_json("rules.json").to_dict()
        self.enable_computer = enable_computer
        self.scoreboard = scoreboard

    def start_game(self):
        self.initialise_game()
        self.game_loop()
    
    # Initialise game prints the welcome to the terminal to introduce the player to the game
    # Player's name is taken as input to terminal
    def initialise_game(self):
        PrintUtils.print_slowly("Welcome to Rock, Paper, Scissors, Lizard, Spock")

        if len(SaveUtils.get_saves()) > 0:
            selected_save = self.start_from_save()

        if not selected_save:
            self.player1_name = InputUtils.take_input(
                "What is your name?", 
                "Name",
                "name",
                False
            )
            PrintUtils.print_slowly("Welcome {}".format(self.player1_name))
            mode_choice = None
            confirmation = None
            while mode_choice is None:
                PrintUtils.print_slowly("Would you like to play against the computer " + colored("[C]", "green") + " or another player " + colored("[P]", "green") + " locally?")
                mode_choice = input("[" + colored("C", "green") + "/" + colored("P", "green") + "]: ").lower()
                if mode_choice == "computer" or mode_choice == "c":
                    confirmation = InputUtils.take_yes_no_input("You have chosen to play against the computer, are you sure?")
                    if not confirmation:
                        mode_choice = None
                        continue
                    self.enable_computer = True
                elif mode_choice == "player" or mode_choice == "p":
                    confirmation = InputUtils.take_yes_no_input("You have chosen to play against another player locally, are you sure?")
                    if not confirmation:
                        mode_choice = None
                        continue
                    self.enable_computer = False
                else:
                    PrintUtils.print_invalid_input()
                    mode_choice = None
                    continue

                if not self.enable_computer:
                    self.player2_name = InputUtils.take_input(
                        "Player 2, what is your name?",
                        "Name",
                        "name",
                        False
                    )
                else:
                    self.player2_name = "The Computer"
        
            PrintUtils.print_slowly("The game will now start...")
            time.sleep(1.5)
            os.system('cls' if os.name == 'nt' else 'clear')

    def start_from_save(self):
        if InputUtils.take_yes_no_input("Do you want to start from a previous save?", False):
            saves = SaveUtils.get_saves()
            PrintUtils.print_options(saves)
            save_choice = InputUtils.get_user_input_on_options(saves, "That is not a valid save, please enter the corresponding number")
            save = SaveUtils.get_save(saves[int(save_choice)])
            self.player1_name = save["player1"]
            self.player2_name = save["player2"]
            self.enable_computer = save["enable_computer"]
            self.scoreboard = Scoreboard(save["p1_score"], save["p2_score"], save["round"])
            return True
        else:
            return False

    # compute_logic() takes as input
    # player1_input: a parameter of type String that is used to compare against player2_input
    # player2_input: a parameter of type String that is used to compare against player1_input
    # Outputs a number from 0 to 2, where 2 means a tie, 1 means player1 wins, and 0 means player1 loses
    def compute_logic(self, player1_input, player2_input):
        p1_defeats = self.logic_dict[player1_input]['Defeats']
        p1_description = self.logic_dict[player1_input]['Description']
        p2_defeats = self.logic_dict[player2_input]['Defeats']
        p2_description = self.logic_dict[player2_input]['Description']
        
        if player1_input == player2_input:
            return 2
        elif player2_input in p1_defeats:
            PrintUtils.print_slowly("{} {}".format(player1_input, p1_description[p1_defeats.index(player2_input)]))
            return 1
        else:
            PrintUtils.print_slowly("{} {}".format(player2_input, p2_description[p2_defeats.index(player1_input)]))
            return 0

    def play_round(self):
        if self.enable_computer:
            PrintUtils.print_slowly("Please make your choice")
            p1_choice = InputUtils.get_move_choice(self.logic_dict)
            p2_choice = list(self.logic_dict.keys())[random.randrange(len(self.logic_dict))]
        else:
            PrintUtils.print_slowly("It is {}'s turn to make a choice".format(self.player1_name))
            p1_choice = InputUtils.get_move_choice_secretly(self.player1_name, self.logic_dict)
            PrintUtils.print_slowly("It is {}'s turn to make a choice".format(self.player2_name))
            p2_choice = InputUtils.get_move_choice_secretly(self.player2_name, self.logic_dict)

        result = self.compute_logic(p1_choice, p2_choice)
        if result == 2:
            PrintUtils.print_slowly("It's a tie!")
        else:
            PrintUtils.print_slowly("{} wins!".format(self.player1_name if result == 1 else self.player2_name))
        if result == 1:
            self.scoreboard.increment_p1_score()
        elif result == 0:
            self.scoreboard.increment_p2_score()

    def restart_game(self):
        # Autosave
        SaveUtils.autosave(
            self.player1_name, 
            self.player2_name, 
            self.scoreboard, 
            self.enable_computer
        )
        self.scoreboard = Scoreboard()
    
    def game_loop(self):
        while True:
            PrintUtils.print_slowly("It is currently round {}".format(self.scoreboard.get_round()))
            PrintUtils.print_slowly("The score is {} with {} points vs {} with {} points".format(self.player1_name, self.scoreboard.get_p1_score(), self.player2_name, self.scoreboard.get_p2_score()))
            self.play_round()
            self.scoreboard.increment_round()

            play_on = InputUtils.take_yes_no_input("Would you like to keep playing?", False)
            if play_on:
                PrintUtils.print_slowly("The game will continue :)")
            else:
                PrintUtils.print_slowly("Thank you for playing!")
            
            if play_on and InputUtils.take_yes_no_input("Would you like to restart your game?", False):
                self.restart_game()

            if InputUtils.take_yes_no_input("Would you like to save your game?", False):
                while True:
                    save_name = InputUtils.take_input(
                        "What should your save be called?", 
                        "Save Name",
                        "",
                        True,
                        False
                    )

                    if len(save_name.strip()) == 0:
                        PrintUtils.print_slowly("Save names cannot be empty!")
                        save_name = None
                        continue
                    else:
                        if save_name.replace(" ", "_") in SaveUtils.get_saves():
                            overwrite = InputUtils.take_yes_no_input("Do you want to overwrite your save {}?".format(save_name), False)
                            if overwrite:
                                SaveUtils.overwrite_save(
                                    save_name, 
                                    self.player1_name, 
                                    self.player2_name, 
                                    self.scoreboard, 
                                    self.enable_computer
                                )
                                break
                            else:
                                PrintUtils.print_slowly("Please enter a new name")
                                continue
                        else:
                            SaveUtils.create_save(
                                save_name, 
                                self.player1_name, 
                                self.player2_name, 
                                self.scoreboard, 
                                self.enable_computer
                            )
                            PrintUtils.print_slowly("Saved!")
                            time.sleep(1.5)
                            break
            if not play_on:
                SaveUtils.autosave(
                    self.player1_name, 
                    self.player2_name, 
                    self.scoreboard, 
                    self.enable_computer
                )
                PrintUtils.print_slowly("Autosaved!")
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
