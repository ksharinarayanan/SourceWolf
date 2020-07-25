import os


class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CYAN = "\033[1;36m"

def disableColorsForWindows():
    if os.name == "nt":
        Colors.BLUE = Colors.GREEN = Colors.YELLOW = Colors.RED = Colors.RESET = Colors.BOLD = Colors.CYAN = ""
