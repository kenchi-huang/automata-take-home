from Utils.PrintUtils import PrintUtils
from termcolor import colored
from getpass import getpass
import pandas as pd

class InputUtils:
    @classmethod
    def get_user_input_on_options(self, options, error_message, secret = False):
        output = None
        while output is None:
            if not secret:
                choice = input("[" + colored("0", "green") + "-" + colored("{}".format(len(options) - 1), "green") + "]: ")
            else:
                choice = getpass("[" + colored("0", "green") + "-" + colored("{}".format(len(options) - 1), "green") + "]: ")
            try:
                if type(eval(choice)) == int:
                    if int(choice) < len(options) and int(choice) >= 0:
                        return int(choice)
                    else:
                        PrintUtils.print_slowly(error_message)
                        PrintUtils.print_options(options)
                else:
                    PrintUtils.print_slowly(error_message)
                    PrintUtils.print_options(options)
            except: 
                PrintUtils.print_slowly(error_message)
                PrintUtils.print_options(options)

    @classmethod
    def get_move_choice(self, logic_dict):
        PrintUtils.print_options(logic_dict.keys())
        PrintUtils.print_slowly("What choice will you make?")
        selected_move = self.get_user_input_on_options(logic_dict.keys(), "That is not a valid move, please enter the corresponding number")
        return list(logic_dict.keys())[int(selected_move)]
    
    @classmethod
    def get_move_choice_secretly(self, player_name, logic_dict):
        PrintUtils.print_options(logic_dict.keys())
        PrintUtils.print_slowly("What choice will {} make?".format(player_name))
        selected_move = self.get_user_input_on_options(logic_dict.keys(), "That is not a valid move, please enter the corresponding number", True)
        return list(logic_dict.keys())[int(selected_move)]

    @classmethod
    def take_input(self, question, input_text, question_context, is_choice_question = False, confirm = True):
        output = ""
        yes_no_question = ""
        while len(output) == 0:
            PrintUtils.print_slowly(question)
            output = input("[" + colored(input_text, "green") + "]: ")
            choice = None
            if confirm:
                if not is_choice_question:
                    yes_no_question = "Is {} your {}?".format(output, question_context)
                else:
                    yes_no_question = "You have chosen {}, are you sure?".format(question_context)
                if self.take_yes_no_input(yes_no_question):
                    return output
                else:
                    output = ""
            else:
                return output
    
    @classmethod
    def take_yes_no_input(self, question, is_confirmation = True):
        choice = None
        while choice is None:
            PrintUtils.print_slowly(question)
            choice = input("[" + colored("Y", "green") + "/" + colored("N", "green") + "]: ").lower()
            if choice == "y":
                return True
            elif choice == "n":
                if is_confirmation:
                    PrintUtils.print_slowly("Please enter your choice again")
                return False
            else:
                PrintUtils.print_invalid_input()
                choice = None