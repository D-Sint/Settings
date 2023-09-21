#!/usr/bin/env python3
import argparse
import random
import string
from colorama import Fore


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", dest="lengh", help="Count of password lenght")
    return parser.parse_args()

options = get_args()
lenght_pass = int(options.lengh)
ascii_lett = [x for x in (string.ascii_letters + string.digits)]

random.shuffle(ascii_lett)

full_pass = ''.join((random.choices(ascii_lett, k=lenght_pass)))

print(Fore.GREEN + "passwd:",  Fore.LIGHTRED_EX + full_pass)
