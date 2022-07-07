#!/usr/bin/env python3
from pathlib import Path
import os

import click

from test_tools.common import execute_pipe

@click.command
@click.argument('executable', type=click.Path(exists=True))
@click.argument('test_folder', type=click.Path(exists=True))
def main(executable, test_folder):
    print(test_folder)
    for f in os.listdir(test_folder):
        f = Path(test_folder) / f
        if f.is_file() and f.suffix == '.txt':
            print(f"doing {f.name}")
            outfile = Path(f.parent) / f.name.replace('.txt', '.output.txt')
            fil = outfile.open('w+')
            execute_pipe(f"cat {f} | {executable}", fil)

if __name__ == '__main__':
    main()
