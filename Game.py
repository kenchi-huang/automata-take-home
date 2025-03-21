import time
import sys
import os
import pandas as pd
from Scoreboard import Scoreboard
from Save import Save
from getpass import getpass
import random
import datetime

class Game:
    def __init__(self, scoreboard = Scoreboard(), restart = False, player1_name = "", player2_name = "", enable_computer = True):
        self.restart = restart
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.logic_dict = pd.read_json("rules.json").to_dict()
        self.enable_computer = enable_computer
        self.scoreboard = scoreboard
        self.save = Save()
        self.invalid_input_string = "That was not a valid input, please try again"

    def print_slowly(self, text):
        for idx, char in enumerate(text):
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(.03)
        print()

    def start_game(self):
        self.initialise_game()
        self.game_loop()

    def take_input(self, question, input_text, question_context, is_choice_question = False, confirm = True):
        output = ""
        yes_no_question = ""
        while len(output) == 0:
            self.print_slowly(question)
            output = input(input_text)
            choice = None
            if confirm:
                if not is_choice_question:
                    yes_no_question = "Is {} your {}".format(output, question_context)
                else:
                    yes_no_question = "You have chosen {}, are you sure?".format(question_context)
                if self.take_yes_no_input(yes_no_question):
                    return output
                else:
                    output = ""
            else:
                return output
    
    def take_yes_no_input(self, question, is_confirmation = True):
        choice = None
        while choice is None:
            self.print_slowly(question)
            choice = input("[Y/N]: ").lower()
            if choice == "y":
                return True
            elif choice == "n":
                if is_confirmation:
                    self.print_slowly("Please enter your choice again")
                return False
            else:
                self.print_slowly(self.invalid_input_string)
                choice = None
    
    # Initialise game prints the welcome to the terminal to introduce the player to the game
    # Player's name is taken as input to terminal
    def initialise_game(self):
        self.print_slowly("Welcome to Rock, Paper, Scissors, Lizard, Spock")

        

        self.player1_name = self.take_input(
            "What is your name?", 
            "[Name]: ",
            "name",
            False
        )
        self.print_slowly("Welcome {}".format(self.player1_name))
        mode_choice = None
        confirmation = None
        while mode_choice is None:
            self.print_slowly("Would you like to play against the computer [C] or another player [P] locally?")
            mode_choice = input().lower()
            if mode_choice == "computer" or mode_choice == "c":
                confirmation = self.take_yes_no_input("You have chosen to play against the computer, are you sure?")
                if not confirmation:
                    mode_choice = None
                    continue
                self.enable_computer = True
            elif mode_choice == "player" or mode_choice == "p":
                confirmation = self.take_yes_no_input("You have chosen to play against another player locally, are you sure?")
                if not confirmation:
                    mode_choice = None
                    continue
                self.enable_computer = False
            else:
                self.print_slowly(self.invalid_input_string)
                mode_choice = None
                continue

            if not self.enable_computer:
                self.player2_name = self.take_input(
                    "What is the other player's name?",
                    "[Name]: ",
                    "name",
                    False
                )
            else:
                self.player2_name = "The Computer"
            
            self.print_slowly("The game will now start...")
            time.sleep(1.5)
            os.system('cls' if os.name == 'nt' else 'clear')

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
            self.print_slowly("{} {}".format(player1_input, p1_description[p1_defeats.index(player2_input)]))
            return 1
        else:
            self.print_slowly("{} {}".format(player2_input, p2_description[p2_defeats.index(player1_input)]))
            return 0

    def print_options(self):
        for index, key in enumerate(self.logic_dict.keys()):
            self.print_slowly("[{}] {}".format(index, key))

    def get_move_choice(self):
        self.print_options()
        selected_move = None
        self.print_slowly("What choice will you make?")
        while selected_move is None:
            move_choice = input("[0-{}]: ".format(len(self.logic_dict) - 1))
            try:
                if type(eval(move_choice)) == int:
                    if int(move_choice) < len(self.logic_dict.keys()):
                        return list(self.logic_dict.keys())[int(move_choice)]
                    else:
                        self.print_slowly("That is not a valid move, please enter the corresponding number")
                        self.print_options()
                else:
                    self.print_slowly("That is not a valid move, please enter the corresponding number")
                    self.print_options()
            except:
                self.print_slowly("That is not a valid move, please enter the corresponding number")
                self.print_options()

    
    def get_move_choice_secretly(self, player_name):
        self.print_options()
        selected_move = None
        self.print_slowly("What choice will {} make?".format(player_name))
        while selected_move is None:
            move_choice = getpass("[0-{}]: ".format(len(self.logic_dict) - 1))
            try:
                if type(eval(move_choice)) == int:
                    if int(move_choice) < len(self.logic_dict.keys()):
                        return list(self.logic_dict.keys())[int(move_choice)]
                    else:
                        self.print_slowly("That is not a valid move, please enter the corresponding number")
                        self.print_options()
                else:
                    self.print_slowly("That is not a valid move, please enter the corresponding number")
                    self.print_options()
            except:
                self.print_slowly("That is not a valid move, please enter the corresponding number")
                self.print_options()

    def play_round(self):
        if self.enable_computer:
            self.print_slowly("Please make your choice")
            p1_choice = self.get_move_choice()
            p2_choice = list(self.logic_dict.keys())[random.randrange(len(self.logic_dict))]
        else:
            self.print_slowly("It is {}'s turn to make a choice".format(self.player1_name))
            p1_choice = self.get_move_choice_secretly(self.player1_name)
            self.print_slowly("It is {}'s turn to make a choice".format(self.player2_name))
            p2_choice = self.get_move_choice_secretly(self.player2_name)

        result = self.compute_logic(p1_choice, p2_choice)
        if result == 2:
            self.print_slowly("It's a tie!")
        else:
            self.print_slowly("{} wins!".format(self.player1_name if result == 1 else self.player2_name))
        if result == 1:
            self.scoreboard.increment_p1_score()
        elif result == 0:
            self.scoreboard.increment_p2_score()

    def restart_game(self):
        # Autosave
        self.autosave()
        self.scoreboard = Scoreboard(self.player1_name, self.player2_name)
    
    def autosave(self):
        self.save.create_save("Autosave", self.player1_name, self.player2_name, self.scoreboard, self.enable_computer)

    def game_loop(self):
        while True:
            self.print_slowly("It is currently round {}".format(self.scoreboard.get_round()))
            self.print_slowly("The score is {} with {} points vs {} with {} points".format(self.player1_name, self.scoreboard.get_p1_score(), self.player2_name, self.scoreboard.get_p2_score()))
            self.play_round()
            self.scoreboard.increment_round()

            play_on = self.take_yes_no_input("Would you like to keep playing?", False)
            if play_on:
                self.print_slowly("The game will continue :)")
            else:
                self.print_slowly("Thank you for playing!")
            
            if play_on and self.take_yes_no_input("Would you like to restart your game?", False):
                self.restart_game()

            if self.take_yes_no_input("Would you like to save your game?", False):
                while True:
                    save_name = self.take_input(
                        "What should your save be called?", 
                        "[ENTER NAME]: ",
                        "",
                        True,
                        False
                    )

                    if len(save_name.strip()) == 0:
                        self.print_slowly("Save names cannot be empty!")
                        save_name = None
                        continue
                    else:
                        if save_name.replace(" ", "_") in self.save.get_saves():
                            overwrite = self.take_yes_no_input("Do you want to overwrite your save {}?".format(save_name_choice), False)
                            if overwrite:
                                self.save.overwrite_save(save_name)
                            else:
                                self.print_slowly("Please enter a new name")
                                continue
                        else:
                            self.save.create_save(save_name, self.player1_name, self.player2_name, self.scoreboard, self.enable_computer)
                            self.print_slowly("Saved!")
                            break
            if not play_on:
                self.autosave()
                self.print_slowly("Autosaved!")
                break

    def debug(self):
        print(random.randrange(len(self.logic_dict)))

game = Game()
game.start_game()