#!/env/python

import argparse
from subprocess import os, PIPE, run
from ont_fast5_api.fast5_interface import get_fast5_file
from ont_fast5_api.conversion_tools.fast5_subset import Fast5Filter


def parse_args():
    parser = argparse.ArgumentParser(description="remove skipped reads from fast5 files")
    parser.add_argument("dir", type="str", help="path to fast5 files")
    parser.add_argument("out", type="str", help="path to save cleaned fast5 files")
    parser.add_argument("threads", type="int", )
    return parser.parse_args()

def find_files(path):
    all_files = run(["ls", f"{path}"], stdout=PIPE).stdout.decode("utf-8").rstrip().split("\n")
    fast5_files = []
    for f in all_files:
        if f.endswith(".fast5"):
            fast5_files.append(f)
    return fast5_files

def extract_basecalled_reads(file):
    with get_fast5_file(file, mode="r") as f5:
        basecalled_reads = []
        for read in f5.get_reads():
            analysis = read.list_analyses()
            if ('basecall_1d', 'Basecall_1D_000') in analysis:
                basecalled_reads.append(read)
    return basecalled_reads

def main():
    args = parse_args()
    input = os.path.abspath(args.dir)
    output = os.path.abspath(args.out)
    
    fast5_files = find_files(input)
    
    with open("read_list_file.txt", "w+") as o:
        for file in fast5_files:
            o.write(extract_basecalled_reads(file))
    
if __name__ == '__main__':
    main()