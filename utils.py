from google.genai import types
from config import GRAY, RESET

def print_one_message(msg: types.Content):
    print(f"{GRAY}{msg.role}:{RESET}")
    for part in (msg.parts or []):
        if not part:
            continue
        formatted = format_part(part)
        # Indent multiline text for readability
        formatted = "\n  ".join(formatted.splitlines())
        print(f"  {GRAY}{formatted}{RESET}")
    print()  # blank line between messages


def print_messages(messages: list[types.Content]):
    for msg in messages:
        print_one_message(msg)


def check_args(args: list[str], verbose: dict[str, bool]):
    if len(args) < 2:
        print("Usage: python main.py <prompt>")
        exit(1)
    if len(args) > 2 and args[2] == "--verbose":
        verbose["value"] = True


def format_part(part: types.Part) -> str:
    if part.text:
        return f"\"{part.text}\""
    if part.function_call:
        return f"function_call: {part.function_call.name} {part.function_call.args}"
    if part.function_response:
        # Extract the 'result' field if present to preserve line breaks
        resp = getattr(part.function_response, "response", None)
        if isinstance(resp, dict) and "result" in resp:
            return f"function_response: \n{resp['result']}"
        return f"function_response: \n{resp}"
    if part.code_execution_result:
        return f"code_execution_result: {part.code_execution_result}"
    if part.executable_code:
        return f"executable_code: {part.executable_code.code}"
    if part.inline_data:
        return f"inline_data: {part.inline_data}"
    if part.file_data:
        return f"file_data: {part.file_data}"
    if part.video_metadata:
        return f"video_metadata: {part.video_metadata}"
    if part.thought:
        return f"thought: {part.thought}"
    return "<empty>"

