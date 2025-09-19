from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
import os
import sys

def get_system_prompt() -> str:
    sys_prompt: str = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    return sys_prompt


def check_args(args: list[str], verbose: dict[str, bool]):
    if len(args) < 2:
        print("Usage: python main.py <prompt>")
        exit(1)
    if len(args) > 2 and args[2] == "--verbose":
        verbose["value"] = True


def print_res(res: types.GenerateContentResponse, verbose: dict[str, bool], user_prompt: str):
    if verbose["value"] == True:
        print(f"User prompt: {user_prompt}")
        if res.usage_metadata:
            print(
            f"Prompt tokens: {res.usage_metadata.prompt_token_count}\n"
        )
    if res.function_calls:
        for func_call in res.function_calls:
            # print(f"Calling function: {func_call.name}({func_call.args})")
            err = call_function(func_call, verbose["value"])
            if err != None:
                return err
    if res:
        print(res.text)
    if res.usage_metadata and verbose["value"] == True:
        print(
            f"Response tokens: {res.usage_metadata.candidates_token_count}\n"
        )


def main():
    verbose = {"value": False}
    check_args(sys.argv, verbose)
    _ = load_dotenv()

    # --- Setup vars ---
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = str(os.getenv("GEMINI_MODEL"))
    user_prompt = sys.argv[1]
    system_prompt = get_system_prompt()
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )


    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    client = genai.Client(api_key=api_key)
    res = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    print_res(res, verbose, user_prompt)



if __name__ == "__main__":
    main()
