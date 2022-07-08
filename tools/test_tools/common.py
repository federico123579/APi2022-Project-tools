import subprocess
from subprocess import PIPE
import shlex
from pathlib import Path

def execute_pipe(cmd_str: str, final_stdout = None) -> int:
    """rudimental & unsafe utility function"""
    if '|' not in cmd_str:
        raise ValueError("pipe not present")
    parts: list[list[str]] = [shlex.split(x) for x in cmd_str.split('|')]
    p_old = subprocess.Popen(parts[0], stdout=PIPE)

    final_flag = False
    return_value = 0
    for i, to_pipe in enumerate(parts[1:]):
        if i == len(parts) - 2: # final cmd
            final_flag = True
            stdout = final_stdout
        else:
            stdout = PIPE

        p = subprocess.Popen(to_pipe, stdout=stdout, stdin=p_old.stdout)

        if final_flag:
            return_value = p.wait()
        else:
            p_old = p

    return return_value

def tested_correctly(test_input: Path, test_output: Path, executable_path: Path) -> bool:
    res = execute_pipe(f"cat {test_input} | {executable_path} | cmp -s {test_output}")
    if res == 0:
        return True
    else:
        return False

