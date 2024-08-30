#!/usr/bin/env python3
import sys
from colorama import Fore, Style
from analyze_text import analyze_text
from metrics.nlp import nlp_pipe


COLOR_MAP = {
    20: Fore.RED + Style.DIM,
    30: Fore.RED + Style.NORMAL,
    40: Fore.RED + Style.BRIGHT,
    50: Fore.YELLOW + Style.DIM,
    60: Fore.YELLOW + Style.NORMAL,
    70: Fore.YELLOW + Style.BRIGHT,
    80: Fore.GREEN + Style.DIM,
    90: Fore.GREEN + Style.NORMAL,
    100: Fore.GREEN + Style.BRIGHT,
}


def score_to_color(score):
    for score_limit, color in COLOR_MAP.items():
        if min(score, max(COLOR_MAP)) > score_limit:
            continue
        print(color, end="")
        return
    assert False, "if reach here, something is wrong"


def print_text():
    for sentence in nlp_pipe("en")(sys.stdin.read()).sents:
        score_to_color(analyze_text(str(sentence), language="en", use_llm=False)["flesch-reading-ease"]["score"])
        print(sentence, end="")
    print(Style.RESET_ALL, end="")


def print_legend():
    print()
    print("Legend:")
    print("  ", end='')
    for score in COLOR_MAP:
        score_to_color(score)
        print("###", end='')
    print(Style.RESET_ALL, end="")
    print()
    print('  not readable <---> readable')


if __name__ == "__main__":
    print_text()
    print_legend()
