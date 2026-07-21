import time as te

import fire

from .cli import Rag

RED = '\033[0;31m'
RESET = '\033[1;37m'
BLUE = "\033[34m"
GREEN = "\033[92m"
GRAY = '\033[37m'
DIAMOND = "\033[0;93;1;40m"


def logo_animated() -> None:
    """   RAG LOGO ANIMATED """
    with open("src/logo", "r") as logo:
        lines = logo.read().splitlines()
        for line in lines:
            print(f"{DIAMOND}{line}{RESET}", flush=True)
            te.sleep(0.1)


def main() -> None:
    """the main functions where the code starts"""
    logo_animated()
    fire.Fire(Rag)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{RED}{e}{RESET}")

    except KeyboardInterrupt:
        pass
