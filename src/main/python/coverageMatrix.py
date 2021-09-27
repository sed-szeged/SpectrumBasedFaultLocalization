import subprocess
import json
import sys

import testFiles
import os

cov_matrix = {}


def run_this_command(command):
    command = str(' ').join(command)
    subprocess.run(command, shell=True)


def get_coverage_json(path):
    test_folder, tests_folder, test_files, tests_files = testFiles.get_TestFiles(path)
    command = ["coverage", "run", "--source=\"" + path + "\"", "--rcfile=.coveragerc", "-m", "pytest"]
    for file in tests_files:
        command.append("\"" + path + os.path.sep + tests_folder + os.path.sep + file + "\"")
    for file in test_files:
        command.append("\"" + path + os.path.sep + test_folder + os.path.sep + file + "\"")
    print(command)

    run_this_command(command)
    command = ['coverage', 'json', '--show-contexts']
    print(command)
    run_this_command(command)


def make_cov_matrix(res_dict, path):
    for key in res_dict.keys():
        print("yo_key",key)
        cov_matrix[key] = []

    if not os.path.exists("coverage.json"):
        get_coverage_json(path)


    if os.path.exists("method_cov.json") and not os.stat("method_cov.json").st_size == 0:
        if os.path.exists("class_cov.json") and not os.stat("class_cov.json").st_size == 0:

            with open("class_cov.json", 'r') as class_cov_json:
                class_data = json.load(class_cov_json)
                with open("coverage.json", 'r') as cov_json:
                    with open("method_cov.json", 'r') as method_cov_json:
                        method_data = json.load(method_cov_json)
                        statement_data = json.load(cov_json)
                        for file in statement_data["files"]:

                            for _class in class_data["files"][file]["contexts"]:
                                start_line = int(class_data["files"][file]["contexts"][_class]["start_line"])
                                last_line = int(class_data["files"][file]["contexts"][_class]["end_line"])

                                for statement in statement_data["files"][file]["contexts"]:
                                    method_name = ""
                                    for method in method_data["files"][file]["contexts"]:
                                        method_start_line = int(method_data["files"][file]["contexts"][method]["start_line"])
                                        method_last_line = int(method_data["files"][file]["contexts"][method]["end_line"])
                                        if method_start_line <= int(statement) <= method_last_line:
                                            method_name = method

                                    if start_line <= int(statement) <= last_line:
                                        tcs = statement_data["files"][file]["contexts"][statement]
                                        try:
                                             for tc in tcs:

                                                tc = tc.replace('.', os.path.sep, 1)


                                                cov_matrix[tc].append(str(file + ":"+ _class +":" +method_name + ":"+ statement))
                                        except:
                                            pass
        else:
            with open("method_cov.json", 'r') as method_cov_json:
                method_data = json.load(method_cov_json)
                with open("coverage.json", 'r') as cov_json:
                    statement_data = json.load(cov_json)
                    for file in statement_data["files"]:

                        for method in method_data["files"][file]["contexts"]:

                            method_tcs = method_data["files"][file]["contexts"][method]["tc"]
                            start_line = int(method_data["files"][file]["contexts"][method]["start_line"])
                            last_line = int(method_data["files"][file]["contexts"][method]["end_line"])
                            print(method, start_line, last_line)
                            for statement in statement_data["files"][file]["contexts"]:

                                if start_line <= int(statement) <= last_line:
                                    print(statement)
                                    tcs = statement_data["files"][file]["contexts"][statement]
                                    #print(tcs)
                                    try:

                                        for tc in tcs:

                                            tc = tc.replace('.', os.path.sep, 1)
                                            print(tc)
                                            print(str(file + ":" +method + ":" + statement))
                                            print("MIAFASZ", cov_matrix[tc])

                                            cov_matrix[tc].append(str(file + ":" +method + ":" + statement))
                                        print("This is mething,", cov_matrix)
                                    except Exception as ex:
                                        print("Dasistexception",ex)
                                        pass

    else:
        with open("coverage.json", 'r') as cov_json:
            data = json.load(cov_json)
            for file in data["files"]:
                print(data["files"][file]["contexts"])
                for statement in data["files"][file]["contexts"]:
                    tcs = data["files"][file]["contexts"][statement]
                    print(file, statement)
                    try:
                        for tc in tcs:
                            if str(tc) == '':
                                raise Exception
                            if tc not in cov_matrix:
                                cov_matrix[tc] = [str(file + ":" + statement)]
                            else:
                                cov_matrix[tc].append(str(file + ":" + statement))
                    except:
                        pass

    if cov_matrix:
        print(cov_matrix)
        with open("coverage_matrix.json", "w") as outfile:
            print(cov_matrix)
            json.dump(cov_matrix, outfile)
            return cov_matrix
    else:
        #raise Exception('No coverage matrix collected!')
        sys.exit(4)