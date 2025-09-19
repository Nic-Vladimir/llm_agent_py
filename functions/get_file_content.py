import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the specified's file content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read from, relative to the working directory.",
            ),
        },
    ),
)

def validate_file(working_directory: str, file_path: str) -> str | None:
    try:
        file_path_abs = os.path.abspath(file_path)
        working_directory_abs = os.path.abspath(working_directory)
        if os.path.commonpath([working_directory_abs, file_path_abs]) != working_directory_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        return f"Error: {e}"
    return None

def get_file_content(working_directory: str, file_path: str) -> str:
    file_path = os.path.join(working_directory, file_path)
    err = validate_file(working_directory, file_path)
    if err != None:
        return err

    MAX_CHARS = 10000
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read(MAX_CHARS)
        if len(file_content) == MAX_CHARS:
            file_content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content
    except Exception as e:
        return f"Error: {e}"
