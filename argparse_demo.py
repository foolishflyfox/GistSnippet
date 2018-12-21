#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    description='Some description about this script',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,  # show default value
)
# add required option. Note: required option can't with default parameter
parser.add_argument('info', type=str, help="required option")
# optional option, should follow by a value
parser.add_argument('-c', '--count', type=int, default=20,
                    help="required option with default value")
# optional option, just used as a flag
parser.add_argument('-f', '--flag', action='store_true', help="flag option")


opt = parser.parse_args()

print(f'opt.info : {opt.info}')
print(f'opt.count : {opt.count}')
print(f'opt.flag : {opt.flag}')

# Experimental Effect

# Experiment 1
# ~$ argparse_demo.py -h
# usage: argparse_demo.py [-h] [-c COUNT] [-f] info

# Some description about this script

# positional arguments:
#   info                  required option

# optional arguments:
#   -h, --help            show this help message and exit
#   -c COUNT, --count COUNT
#                         required option with default value (default: 20)
#   -f, --flag            flag option (default: False)

# Experiment 2
# ~$ argparse_demo.py "hello , world"
# opt.info : hello , world
# opt.count : 20
# opt.flag : False

# Experiment 3
# ~$ argparse_demo.py -f -c 12 "hello , world"
# opt.info : hello , world
# opt.count : 12
# opt.flag : True

