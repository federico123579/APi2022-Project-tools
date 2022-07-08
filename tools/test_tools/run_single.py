#!/usr/bin/env python3
import os
from pathlib import Path
import shlex
from subprocess import PIPE, Popen

import click

from rich.console import Console
from rich.text import Text

from test_tools.common import execute_pipe, tested_correctly

def print_diff(text: str, console: Console):
    t = Text(text)
    console.print(t)

def print_bold(text: str, console: Console):
    t = Text(text, "bold")
    console.print(t)

def look_for_diffs_sbs(output_to_validate: Path, corrected_output: Path, console: Console) -> None:
    args = shlex.split(f"diff -y {output_to_validate} {corrected_output}")
    p = Popen(args, stdout=PIPE)
    if p.stdout is not None:
        for line in p.stdout.readlines():
            l = line.decode().strip('\n')
            print_diff(l, console)
    console.print(Text("\nleft is yours, right is correct", "bold"))

def look_for_diffs(output_to_validate: Path, corrected_output: Path, console: Console) -> None:
    args = shlex.split(f"diff {output_to_validate} {corrected_output}")
    p = Popen(args, stdout=PIPE)
    if p.stdout is not None:
        for line in p.stdout.readlines():
            l = line.decode().strip('\n')
            if l[0] in ['<', '>']:
                print_diff(l, console)
            else:
                print_bold(l, console)
    print_bold("\n< is yours, > is correct", console)

@click.command
@click.argument('executable', type=click.Path(exists=True))
@click.argument('input_test', type=click.Path(exists=True))
@click.argument('correct_output', type=click.Path(exists=True))
@click.option('-y', '--side-by-side', 'sbs', is_flag=True, show_default=True, default=False, help='print diff side by side')
def main(executable, input_test, correct_output, sbs) -> None:
    executable = Path(executable)
    input_test = Path(input_test)
    correct_output = Path(correct_output)
    test_output_file = Path("temp_output_file.txt")

    console = Console()
    if not tested_correctly(input_test, correct_output, executable):
        try:
            fil = test_output_file.open('w+')
            execute_pipe(f"cat {input_test} | {executable}", final_stdout=fil)
            fil.close()
            if sbs:
                look_for_diffs_sbs(test_output_file, correct_output, console)
            else:
                look_for_diffs(test_output_file, correct_output, console)
        except Exception as e:
            raise e
        finally:
            os.remove(test_output_file)
    else:
        console.print(Text("All correct.", "bold green"))



if __name__ == '__main__':
    main()
