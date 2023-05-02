#!/env/python

import argparse
from subprocess import os, PIPE, run
from ont_fast5_api.fast5_interface import get_fast5_file


def parse_args():
    parser = argparse.ArgumentParser(description="remove skipped reads from fast5 files")
    parser.add_argument("in", type="str", help="path to fast5 files")
    parser.add_argument("out", type="str", help="path to save cleaned fast5 files")
    return parser.parse_args()


