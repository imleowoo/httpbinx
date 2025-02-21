"""httpbinx"""

import argparse


def version():
    pass


def server():
    pass


def main():
    parser = argparse.ArgumentParser(
        prog='httpbinx',
        description='httpbinx is a fastapi server for testing.'
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')


if __name__ == '__main__':
    main()
