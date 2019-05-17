import random
import string
from colorama import Fore


def color_red(string):
    return (Fore.RED + string)

def color_blue(string):
    return (Fore.BLUE + string)

def color_green(string):
    return (Fore.GREEN + string)

def GeneratePassword(length):
	return ''.join(random.choice(string.ascii_letters) for i in range(length))