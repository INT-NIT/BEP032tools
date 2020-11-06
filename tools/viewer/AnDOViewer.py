import pandas as pd
import argparse
import os
import sys

def show_struct(directory):
    """
    Show the structure of the directory given in  argument

    Args:
        directory ([Path]): [Path of the directory to show]
    """
    cmd = "tree -d  "+directory
    os.system(cmd)


def show_experiments(directory):
    """
    Show the experiments in the directory given in  argument

    Args:
        directory ([Path]): [Path of the directory to show]
    """
    cmd = "tree -d -L 1 "+directory
    os.system(cmd)


def show_subjects(directory):
    """
    Show the subjects in the directory given in  argument

    Args:
        directory ([Path]): [Path of the directory to show]
    """
    cmd = "tree -d -L 2 "+directory
    os.system(cmd)


def show_sessions(directory):
    """
    Show the sessions in the directory given in  argument

    Args:
        directory ([Path]): [Path of the directory to show]
    """
    cmd = "tree -d -L 3 "+directory
    os.system(cmd)


def main():
    """
    usage: AnDO_Viewer.py [-h] [-S] [-Se] [-Su] [-Ss] pathToDir

    positional arguments:
    pathToDir             Path to the folder to show

    optional arguments:
    -h, --help            show this help message and exit
    -S, --show            show dir structure
    -Se, --show_experiments
                            show experiments folder only
    -Su, --show_subjects  show subjects folder only
    -Ss, --show_sessions  show sessions folder only
    

    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-S', '--show', help=' show dir structure ', action='store_true', default=True)
    parser.add_argument('-Se', '--show_experiments',
                        help=' show experiments folder only', action='store_true')
    parser.add_argument('-Su', '--show_subjects',
                        help='  show subjects folder only', action='store_true')
    parser.add_argument('-Ss', '--show_sessions',
                        help='  show sessions folder only', action='store_true')
    parser.add_argument('pathToDir', help='Path to the folder to show')

    args = parser.parse_args()


    ## Check if directory exists
    if not os.path.isdir(args.pathToDir):
            print('Directory does not exist:', args.pathToDir)
            exit(1)
    if args.show:
                show_struct(args.pathToDir)
    if args.show_experiments:
                show_experiments(args.pathToDir)
    if args.show_subjects:
                show_subjects(args.pathToDir)
    if args.show_sessions:
                show_sessions(args.pathToDir)


if __name__ == '__main__':
    main()
