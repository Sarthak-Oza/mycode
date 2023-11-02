#!/usr/bin/env python3

from os import system
from numpy import average
from colorama import Fore, Back, Style
from questions import questions

CHOICE_MIN = 1
CHOICE_MAX = 5

def ask_question(question, options):
    while True:
        try:
            print(question)
            for option, option_description in options.items():
                print(f"{option}. {option_description}")

            print()
            choice = int(input(Back.GREEN + f"Enter the number of your choice from :" + Style.RESET_ALL + " "))
            print()

            if choice in options:
                return choice
            else:
                print(f"{Fore.RED}######## Please enter a valid option {CHOICE_MIN}-{CHOICE_MAX}. ########{Style.RESET_ALL}")
        except ValueError:
                print(f"{Fore.RED}\n######## Invalid input. Please try again, enter a valid option {CHOICE_MIN}-{CHOICE_MAX}. ########{Style.RESET_ALL}")

def determine_age(answers):
    calculated_age = int(average(list(answer * 15 for answer in answers)))
    return calculated_age

def main():
    while True:
        system("clear")
        print(f"{Fore.YELLOW}{Back.CYAN}{'#' * 19} Welcome to the 'What Age Are You?' Quiz! {'#' * 19}{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}{Back.CYAN}{'#' * 8} Answer the following questions to find out your age mentality. {'#' * 8}{Style.RESET_ALL}\n")


        answers = []
    
        for question, options in questions.items():
            choice = ask_question(question, options)
            answers.append(choice)
            system("clear")

        result = determine_age(answers)
        print(f"{Fore.YELLOW}{Back.BLUE}************  You are {Style.BRIGHT}{result}{Style.NORMAL} years old!  ************{Style.RESET_ALL}", end="\n\n")

        play_again = input("Do you want to play again (press 's' to start over or 'q' to quit)? ").strip().lower()
        if play_again != 's':
            break

if __name__ == "__main__":
    main()