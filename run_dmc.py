#!/usr/bin/python3

from pathlib import Path
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('dir')
parser.add_argument('-c', '--command')
parser.add_argument('-p', '--pattern')
parser.add_argument('--input-replace')
parser.add_argument('--output-replace', default = None)
parser.add_argument('-o', '--output-suffix', default = None)
args = parser.parse_args()


for f in list(Path(args.dir).glob(args.pattern)):
    cmd_split = args.command.split(args.input_replace)

    if args.output_replace is not None:
        f_out = '.'.join(str(f.absolute()).split('.')[:-1] + [args.output_suffix])
        cmd_split = [f_out.join(s.split(args.output_replace)) for s in cmd_split]

    cmd = str(f.absolute()).join(cmd_split)

    print(cmd, file=sys.stderr)
    subprocess.run([cmd], shell = True)

