import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite the specified's file content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the file.",
            )
        },
    ),
)

def validate_path(work_dir_abs: str, full_path_abs: str, file_path: str) -> str | None:
    if os.path.commonpath([work_dir_abs, full_path_abs]) != work_dir_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        os.makedirs(os.path.dirname(full_path_abs), exist_ok=True)
    except Exception as e:
        return f'Error: {e}'
    return None

def write_file(working_directory: str, file_path: str, content: str) -> str:
    full_path = os.path.join(working_directory, file_path)
    full_path_abs = os.path.abspath(full_path)
    work_dir_abs = os.path.abspath(working_directory)

    err = validate_path(work_dir_abs, full_path_abs, file_path)
    if err != None:
        return err
    try:
        with open(full_path, "w") as file:
            _ = file.write(content)
    except Exception as e:
        return f'Error: {e}'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

