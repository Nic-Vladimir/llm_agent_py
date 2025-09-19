from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def get_files_info_tests():
    cases = [
        ("calculator", ".", "current directory"),
        ("calculator", "pkg", "'pkg' directory"),
        ("calculator", "/bin", "'/bin' directory"),
        ("calculator", "../", "'../' directory"),
    ]

    for working_dir, directory, label in cases:
        print(f"Result for {label}:")
        result = get_files_info(working_dir, directory)
        print(result)
        print()

def get_file_content_tests():
    cases = [
        ("calculator", "lorem.txt"),
        ("calculator", "nonexistent.txt"),
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
        ("calculator", "pkg/does_not_exist.py"),
    ]

    for working_dir, file_path in cases:
        print(f"Result for {file_path}:")
        result = get_file_content(working_dir, file_path)
        print(result)
        print()

def write_file_tests():
    cases = [
        ("calculator", "test.txt", "Hello, world!"),
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed"),
    ]

    for working_dir, file_path, content in cases:
        print(f"Result for {file_path}:")
        result = write_file(working_dir, file_path, content)
        print(result)
        print()

def run_python_file_tests():
    cases = [
        ("calculator", "main.py"),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "nonexistent.py"),
        ("calculator", "tests.py"),
        ("calculator", "../main.py"),
    ]

    for working_dir, file_path, *args in cases:
        args_list = args[0] if args else None
        print(f"Result for {file_path}:")
        result = run_python_file(working_dir, file_path, args_list)
        print(result)
        print()

def run_tests():
    # get_files_info_tests()
    # get_file_content_tests()
    # write_file_tests()
    run_python_file_tests()

if __name__ == "__main__":
    run_tests()
