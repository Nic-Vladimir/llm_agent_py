from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def call_function(function_call_part: types.FunctionCall, verbose: bool = False) -> types.Content | None:
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # Pick the function by name
    func_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    func_name = function_call_part.name
    if func_name is None:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name="None",
                response={"error": f"Unknown function: None"},
            )
        ],
    )

    func = func_map.get(func_name)
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )

    # Copy args and inject working directory
    args = function_call_part.args or {}
    args["working_directory"] = "./calculator"

    try:
        result = func(**args)
        print(f"Result:\n{result}")
    except Exception as e:
        print(f"Error while executing {function_call_part.name}: {e}")
    return
