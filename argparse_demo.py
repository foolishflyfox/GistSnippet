#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    description='Some description about this script',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,  # show default value
)
# add required option. Note: required option can't with default parameter
parser.add_argument('info', type=str, help="required option")
# add multi value require option
parser.add_argument('-s', '--source', type=str, required=True, nargs='+',
                    help='required options with multi value')
# optional option, should follow by a value
parser.add_argument('-c', '--count', type=int, default=20,
                    help="optional option with default value")
# optional option, just used as a flag
parser.add_argument('-f', '--flag', action='store_true', help="flag option")
# nargs value such as : '?', '*', '+'
parser.add_argument('-m', '--multi-v', type=int, nargs=2, default=[2,4], 
                    help="multi options")


opt = parser.parse_args()

print(f'opt.info : {opt.info}')
print(f'opt.source : {opt.source}')
print(f'opt.count : {opt.count}')
print(f'opt.flag : {opt.flag}')
print(f'opt.multi_v : {opt.multi_v}')

# Experiments

# Experiment 1
# ~$ argparse_demo.py -h
# usage: argparse_demo.py [-h] -s SOURCE [SOURCE ...] [-c COUNT] [-f]
#                         [-m MULTI_V MULTI_V]
#                         info

# Some description about this script

# positional arguments:
#   info                  required option

# optional arguments:
#   -h, --help            show this help message and exit
#   -s SOURCE [SOURCE ...], --source SOURCE [SOURCE ...]
#                         required options with multi value (default: None)
#   -c COUNT, --count COUNT
#                         optional option with default value (default: 20)
#   -f, --flag            flag option (default: False)
#   -m MULTI_V MULTI_V, --multi-v MULTI_V MULTI_V
#                         multi options (default: [2, 4])
# Experiment 2
# ~$ argparse_demo.py -s sss1 sss2 -f hello,world
# opt.info : hello,world
# opt.source : ['sss1', 'sss2']
# opt.count : 20
# opt.flag : True
# opt.multi_v : [2, 4]

# Experiment 3
# ~$ argparse_demo.py -f -c 12 -m 10 20 'hello, world'
# usage: argparse_demo.py [-h] -s SOURCE [SOURCE ...] [-c COUNT] [-f]
#                         [-m MULTI_V MULTI_V]
#                         info
# argparse_demo.py: error: the following arguments are required: -s/--source

# Experiment 4
# ~$ argparse_demo.py -s sss -f -c 12 -m 10 20 'hello, world'
# opt.info : hello, world
# opt.source : ['sss']
# opt.count : 12
# opt.flag : True
# opt.multi_v : [10, 20]


