import os
import sys


def get_TestFiles(path):
    test_folder = ""
    tests_folder = ""
    test_files = []
    tests_files = []
    if os.path.isdir(path + os.path.sep + "tests"):
        tests_folder = "tests"
    if os.path.isdir(path + os.path.sep + "test"):
        test_folder = "test"

    if tests_folder == "" and test_folder == "":

        sys.exit(2)

    if tests_folder != "":
        with os.scandir(path + os.path.sep + tests_folder) as it:
            for entry in it:
                if not entry.name.startswith('.') and not entry.name == "__init__.py" and entry.is_file() and entry.name.endswith('.py'):

                    tests_files.append(entry.name)

    if test_folder != "":
        with os.scandir(path + os.path.sep + test_folder) as it:
            for entry in it:
                if not entry.name.startswith('.') and not entry.name == "__init__.py" and entry.is_file() and entry.name.endswith(".py"):
                    test_files.append(entry.name)

    return test_folder, tests_folder, test_files, tests_files