import sys
import time
from termcolor import colored

class PrintUtils:
    @classmethod
    def print_slowly(self, text):
        for idx, char in enumerate(text):
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(.03)
        print()

    @classmethod
    def print_invalid_input(self):
        self.print_slowly("That was not a valid input, please try again")

    @classmethod
    def print_options(self, input_list):
        for index, value in enumerate(input_list):
            self.print_slowly("[" + colored("{}".format(index), "green") + "] {}".format(value))