#!/usr/bin/env python3

import sys
import argparse
import os
from .Renamer import Renamer

def main():
    parser = argparse.ArgumentParser(prog='catrename',
                                     description='Rename files according to defined rules.')

    default_categories = os.path.join(os.path.dirname(__file__),
                                      'categories.yaml')
    parser.add_argument('-c',
                        '--categories',
                        metavar='categories',
                        type=str,
                        default=default_categories,
                        help='path to the categories file')
    parser.add_argument('-r',
                        '--recursive',
                        action='store_true',
                        default=False,
                        help='rename files in folders recursively')
    parser.add_argument('-s',
                        '--simulate',
                        action='store_true',
                        default=False,
                        help='output the renames without performing them')
    parser.add_argument('paths',
                        type=str,
                        nargs='+',
                        help='files to rename according to the rules')
    args = parser.parse_args()

    renamer = Renamer(args.categories, args.paths,
                      recursive=args.recursive, simulate=args.simulate)
    renamer.rename()

if __name__ == '__main__':
    main()
