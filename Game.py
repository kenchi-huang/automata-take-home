import time
import sys
import os
import pandas as pd
from Scoreboard import Scoreboard
from getpass import getpass

class Game:
    def __init__(self, restart = False):
        self.restart = restart
        self.player1_name = ""
        self.player2_name = ""
        self.logic_dict = pd.read_json("rules.json").to_dict()
        self.enable_computer = True
        self.scoreboard = None

    def print_slowly(self, text):
        for idx, char in enumerate(text):
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(.03)
        print()

    def start_game(self):
        self.initialise_game()
    
    # Initialise game prints the welcome to the terminal to introduce the player to the game
    # Player's name is taken as input to terminal
    def initialise_game(self):
        self.print_slowly("Welcome to Rock, Paper, Scissors, Lizard, Spock")
        name_choice = None
        while len(self.player1_name) == 0:
            self.print_slowly("What is your name?")
            self.player1_name = input()
            while name_choice != "y" or name_choice != "n":
                self.print_slowly("Is {} your name? [Y/N]".format(self.player1_name))
                name_choice = input().lower()
                if name_choice == "y":
                    break
                elif name_choice == "n":
                    self.print_slowly("Please enter your name again")
                    self.player1_name = ""
                    break
                else:
                    self.print_slowly("Please choose again")

        self.print_slowly("Welcome {}".format(self.player1_name))
        mode_choice = None
        confirmation = None
        while mode_choice is None:
            self.print_slowly("Would you like to play against the computer [C] or another player [P] locally?")
            mode_choice = input().lower()
            if mode_choice == "computer" or mode_choice == "c":
                self.print_slowly("You have chosen to play against the computer, are you sure? [Y/N]")
                confirmation = input().lower()
                self.enable_computer = True
            elif mode_choice == "player" or mode_choice == "p":
                self.print_slowly("You have chosen to play against another player locally, are you sure? [Y/N]")
                confirmation = input().lower()
                self.enable_computer = False
            else:
                self.print_slowly("That is an invalid choice, please try again...")
                mode_choice = None
                continue

            while confirmation != "y" or confirmation != "n":
                if confirmation == "y":
                    self.print_slowly("The game will now start...")
                    time.sleep(1.5)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif confirmation == "n":
                    self.print_slowly("Please choose again")
                    choice = None
                else:
                    self.print_slowly("Please confirm again...")
                    self.print_slowly("Are you sure you want to play against {}? [Y/N]".format("the computer" if self.enable_computer else "another player locally"))
                    confirmation = input().lower()

        if not self.enable_computer:
            while len(self.player2_name) == 0:
                self.print_slowly("What is the other player's name?")
                self.player1_name = input()
                while name_choice != "y" or name_choice != "n":
                    self.print_slowly("Is {} your name? [Y/N]".format(self.player1_name))
                    name_choice = input().lower()
                    if name_choice == "y":
                        break
                    elif name_choice == "n":
                        self.print_slowly("Please enter your name again")
                        self.player1_name = ""
                        break
                    else:
                        self.print_slowly("Please choose again")

        self.scoreboard = Scoreboard(self.player1_name, self.player2_name)

    # compute_logic() takes as input
    # player1_input: a parameter of type String that is used to compare against player2_input
    # player2_input: a parameter of type String that is used to compare against player1_input
    # Outputs a number from 0 to 2, where 2 means a tie, 1 means player1 wins, and 0 means player1 loses
    def compute_logic(self, player1_input, player2_input):
        defeats = self.logic_dict[player1_input]['Defeats']
        
        if player1_input == player2_input:
            return 2
        elif player2_input in defeats:
            return 1
        else:
            return 0

game = Game()
game.start_game()


