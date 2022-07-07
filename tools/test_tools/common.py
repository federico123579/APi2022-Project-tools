import subprocess
import shlex
from pathlib import Path

def execute_pipe(cmd_str: str, final_stdout = None) -> int:
    """rudimental & unsafe utility function"""
    if '|' not in cmd_str:
        raise ValueError("pipe not present")
    parts: list[list[str]] = [shlex.split(x) for x in cmd_str.split('|')]
    p_old = subprocess.Popen(parts[0], stdout=subprocess.PIPE)

    final_flag = False
    return_value = 1
    for i, to_pipe in enumerate(parts[1:]):
        if i == len(parts) - 2: # final cmd
            final_flag = True
            stdout = final_stdout
        else:
            stdout = subprocess.PIPE

        p = subprocess.Popen(to_pipe, stdout=stdout, stdin=p_old.stdout)

        if final_flag:
            return_value = p.wait()
            break

    return return_value

