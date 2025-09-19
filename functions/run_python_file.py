import subprocess
from typing import cast
import sys
import os
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified Python file with the given arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            )
        },
    ),
)

def validate_path(work_dir_abs: str, full_path_abs: str, file_path: str) -> str | None:
    if os.path.commonpath([work_dir_abs, full_path_abs]) != work_dir_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path_abs):
        return f'Error: File "{file_path}" not found.'
    if not full_path_abs.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    return None

def get_formatted_output(status: subprocess.CompletedProcess[str]) -> str:
    stdout = cast(str | None, status.stdout)
    stderr = cast(str | None, status.stderr)

    stdout = stdout.strip() if stdout else ""
    stderr = stderr.strip() if stderr else ""

    parts: list[str] = []
    if stdout:
        parts.append(f"STDOUT: {stdout}")
    if stderr:
        parts.append(f"STDERR: {stderr}")
    if status.returncode != 0:
        parts.append(f"Process exited with code {status.returncode}")
    if not parts:
        return "No output produced"
    return "\n".join(parts)

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    if args is None:
        args = []
    full_path = os.path.join(working_directory, file_path)
    full_path_abs = os.path.abspath(full_path)
    work_dir_abs = os.path.abspath(working_directory)

    err = validate_path(work_dir_abs, full_path_abs, file_path)
    if err != None:
        return err
    try:
        status = subprocess.run(
            [sys.executable, full_path_abs] + args,   # interpreter + script + args
            stdout=subprocess.PIPE,                   # capture stdout
            stderr=subprocess.PIPE,                   # capture stderr
            text=True,                                # decode output as str
            cwd=working_directory,                    # set working dir
            timeout=30                                # avoid infinite runs
        )
        return get_formatted_output(status)
    except subprocess.TimeoutExpired as e:
        return f"Error: Process timed out after {e.timeout} seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"
