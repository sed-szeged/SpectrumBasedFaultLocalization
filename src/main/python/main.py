import getopt
import os
import json
import subprocess
import math
import sys
import shutil
import numpy as np
from scipy.stats import rankdata
import coverageMatrix
import ranking
import testsResults
import metrics
import statistics
import test_res2
import methodCov
import ranking

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hd:", "--directory")
    except getopt.GetoptError:
        print('main.py -d <your_projects_directory>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -d <your_projects_directory>;', 'to start the fault localization process')
            print('main.py -c <file_name>;', 'to get class coverage')
            print('main.py -m <file_name>;', 'to get method coverage')
            print('main.py -s <file_name>;', 'to get the spectrum')
            print('main.py -r <rank_type>;', 'to get certain tie ranking')
            sys.exit()
        elif opt in ("-d", "--directory"):
            path = arg

    copy_rc_file(path)
    os.chdir(path)
    #ranking.scores_ranking(path+"results.json",  "average")
    #sys.exit(0)
    res_dict = testsResults.get_tests_results(path)
    coverageMatrix.get_coverage_json(path)
    #method_cov = methodCov.make_method_cov(path)
    method_cov = {}
    #class_cov = methodCov.make_class_cov(path)
    class_cov = {}
    cov_matrix = coverageMatrix.make_cov_matrix(res_dict, path)
    #print(cov_matrix)

    #method_cov_matrix = coverageMatrix.make_cov_matrix(res_dict, path, 'method')
    counters = statistics.basic_stats(cov_matrix, res_dict)
    print(counters)
    if method_cov and class_cov:
        metrics.make_score_json(counters, method_cov, class_cov)
    elif method_cov and not class_cov:
        metrics.make_score_json(counters, method_cov)
    else:
        metrics.make_score_json(counters)
    #metrics.tarantula(counters)
    #ranking.



def copy_rc_file(path):
    if ".coveragerc" not in os.listdir(path):
        shutil.copyfile(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".coveragerc", path + os.path.sep + ".coveragerc")

    else:
        f = open(path + os.path.sep + ".coveragerc", "r")
        if("[run]" not in f.read()):
            f.close()
            f = open(path + os.path.sep + ".coveragerc", "a")
            f.write("\n")
            f.write("[run]\n")
            f.write("dynamic_context = test_function")
        f.close()

if __name__ == "__main__":
    main(sys.argv[1:])



