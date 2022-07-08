#!/usr/bin/env python3
import glob
from pathlib import Path

import click
from rich.console import Console
from rich.text import Text

from test_tools.common import tested_correctly


def get_test_tuples(test_folder: Path) -> list[tuple[Path, Path]]:
    test_unstructured_files = [Path(l) for l in glob.glob(f"{test_folder}/**/*.txt")]
    test_unstructured_files += [Path(l) for l in glob.glob(f"{test_folder}/*.txt")]
    in_map: dict[str, Path] = {}
    out_map: dict[str, Path] = {}

    for el in test_unstructured_files:
        basename = el.name.split('.')[0]
        if '.output' in el.suffixes:
            out_map[basename] = el
        else:
            in_map[basename] = el

    test_tuples: list[tuple[Path, Path]] = []
    for k, in_f in in_map.items():
        if (out_f := out_map.get(k)) != None :
            test_tuples.append((in_f, out_f))

    return test_tuples

# #################### PRINT ####################
def print_wrong_output(console: Console, in_file: Path, out_file: Path, executable: Path):
    text = Text.assemble(
            f"{in_file.parent.name} ", (f"{in_file.name}", "bold"), " - ", ("FAILED", "bold red"), f"\nprova: testsingle {executable} {in_file} {out_file}")
    console.print(text)

def print_right_output(console: Console, in_file: Path):
    text = Text.assemble(
            f"{in_file.parent.name} ", (f"{in_file.name}", "bold"), " - ", ("SUCCEDED", "bold green"))
    console.print(text)

@click.command
@click.argument('executable', type=click.Path(exists=True))
@click.argument('test_folder', type=click.Path(exists=True))
def main(executable, test_folder):
    console = Console()
    for in_f, out_f in get_test_tuples(Path(test_folder)):
        if not tested_correctly(in_f, out_f, Path(executable)):
            print_wrong_output(console, in_f, out_f, executable)
        else:
            print_right_output(console, in_f)


if __name__ == '__main__':
    main()
