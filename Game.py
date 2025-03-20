import time
import sys
import os
import pandas as pd
from Scoreboard import Scoreboard
from getpass import getpass
import random

class Game:
    def __init__(self, scoreboard, restart = False, player1_name = "", player2_name = "", enable_computer = True):
        self.restart = restart
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.logic_dict = pd.read_json("rules.json").to_dict()
        self.enable_computer = enable_computer
        self.scoreboard = scoreboard

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
        else:
            self.player2_name = "Computer"

        self.scoreboard = Scoreboard(self.player1_name, self.player2_name)

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

    def take_input(self):
        self.print_options()
        selected_move = None
        self.print_slowly("What choice will you make? [Enter a number]")
        while selected_move is None:
            move_choice = input()
            if type(eval(move_choice)) == int:
                if int(move_choice) < len(self.logic_dict.keys()):
                    return list(self.logic_dict.keys())[int(move_choice)]
                else:
                    self.print_slowly("That is not a valid move, please enter the corresponding number")
                    self.print_options()
            else:
                self.print_slowly("That is not a valid move, please enter the corresponding number")
                self.print_options()

    
    def take_secret_input(self, player_name):
        self.print_options()
        selected_move = None
        self.print_slowly("What choice will {} make? [Enter a number]".format(player_name))
        while selected_move is None:
            move_choice = getpass("")
            if type(eval(move_choice)) == int:
                if int(move_choice) < len(self.logic_dict):
                    return list(self.logic_dict.keys())[int(move_choice)]
                else:
                    self.print_slowly("That is not a valid move, please enter the corresponding number")
                    self.print_options()
            else:
                self.print_slowly("That is not a valid move, please enter the corresponding number")
                self.print_options()

    def play_round(self):
        if self.enable_computer:
            self.print_slowly("Please make your choice")
            p1_choice = self.take_input()
            p2_choice = list(self.logic_dict.keys())[random.randrange(len(self.logic_dict))]
        else:
            self.print_slowly("It is {}'s turn to make a choice".format(self.player1_name))
            p1_choice = self.take_secret_input(current_player)
            self.print_slowly("It is {}'s turn to make a choice".format(self.player2_name))
            p2_choice = self.take_secret_input(current_player)

        result = self.compute_logic(p1_choice, p2_choice)
        if result == 2:
            self.print_slowly("It's a tie!")
        else:
            self.print_slowly("{} wins!".format(self.player1_name if result == 1 else "The " + self.player2_name))
        

    def game_loop(self):
        while True:
            self.print_slowly("It is currently round {}".format(self.scoreboard.get_round()))
            self.print_slowly("The score is {} with {} points vs. {} with {} points".format(self.player1_name, self.scoreboard.get_p1_score(), self.player2_name, self.scoreboard.get_p2_score))
            self.play_round()
            self.scoreboard.increment_round()
            play_on_choice = None
            while play_on_choice is None:
                self.print_slowly("Would you like to keep playing? [Y/N]")
                play_on_choice = input().lower()
                if play_on_choice == "y":
                    self.print_slowly("The game will continue :)")
                    break
                elif play_on_choice == "n":
                    self.print_slowly("Thank you for playing!")
                    break
                else:
                    self.print_slowly("That was not a valid input, please try again")
            
            self.print_slowly("Would you like to save your game? [Y/N]")
            # Not implemented

            

    def debug(self):
        print(random.randrange(len(self.logic_dict)))

game = Game(Scoreboard(0, 0))
# game.start_game()
# print(game.take_secret_input("Ken"))

game.play_round()