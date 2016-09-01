#!/usr/bin/env python3

from __future__ import print_function
import configparser
import os.path
from tkinter import *
from tkinter import filedialog
import subprocess


DCRAW_CMD = 'dcraw -v -r 1 1 1 1 -4 -T -S 32767 -k 0 -o 0 -q 0 -t 0'.split()
DEFAULTS = {
    'dcraw': 'dcraw',
    'white_balance': '1 1 1 1',
    'linear_16bit': 'True',
    'tiff_output': 'True',
    'saturation': '32767',
    'dark_level': '0',
    'output_colourspace': '0',
    'interpolation_quality': '0',
    'flip': '0'
}


def make_cmd_line(config):
    dcraw = config['easydcraw'].get('dcraw')
    white_balance = config['easydcraw'].get('white_balance').split()
    saturation = str(config['easydcraw'].get('saturation'))
    dark_level = str(config['easydcraw'].get('dark_level'))
    output_colourspace = str(config['easydcraw'].get('output_colourspace'))
    interpolation_quality = str(config['easydcraw'].get('interpolation_quality'))
    flip = str(config['easydcraw'].get('flip'))
    cmd = [
        dcraw,
        '-S', saturation,
        '-k', dark_level,
        '-o', output_colourspace,
        '-q', interpolation_quality,
        '-t', flip
    ]
    cmd += ['-r'] + white_balance
    if config['easydcraw'].get('linear_16bit'):
        cmd.append('-4')
    if config['easydcraw'].get('tiff_output'):
        cmd.append('-T')
    return cmd


def get_input_files():
    files = filedialog.askopenfilenames(
        filetypes=(("Canon raw images", "*.CR2"), ("All files", "*.*"))
    )
    return files


def convert_with_dcraw(cmd_line, files):
    for f in files:
        subprocess.call(cmd_line + [f])


def read_config():
    config = configparser.ConfigParser(DEFAULTS)
    if not config.has_section('easydcraw'):
        config.add_section('easydcraw')
    config.read(os.path.expanduser('~/.easydcraw.ini'))
    return config


def main():
    Tk().withdraw()
    config = read_config()
    cmd_line = make_cmd_line(config)
    files = get_input_files()
    convert_with_dcraw(cmd_line, files)


if __name__ == '__main__':
    main()
