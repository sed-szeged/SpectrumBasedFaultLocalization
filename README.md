# Call Frequency-Based Fault Localization

This fault localization concept uses as an additional context the frequency of the investigated method occurring in call stack instances during the course of executing the failing test cases.

## The docker image contains:
 - Defects4J bug dataset [(available)](https://github.com/Frenkymd/defects4j/tree/chain)
 - Java instrumenter [(available)](https://github.com/sed-szeged/java-instrumenter/tree/master)
 - measurements framework [(available)](https://github.com/bvancsics/frequencySBFL/tree/main)

## Steps:

 1. Prepare the Docker environment

    - clone this repository
    - build docker:

            docker build -t sbfl .

 2. Create naive and unique count spectra

    - Start docker

            docker run --rm -it sbfl /bin/bash

    - [Docker is running...]

    - Checkout a bug from Defects4J

            defects4j checkout -p [project] -v [bug][version] -w [output folder]

        - For example:

            defects4j checkout -p Lang -v 1b -w Lang_1b

    - Enter bug's directory

            cd [output folder]

        - For example:

            cd Lang_1b

    - Compile project

            defects4j compile

    - Set the coverage data collection granularity to naive count

            export AGENT_GRANULARITY=count

    - Run the tests

            defects4j test

    - Save the coverage data to a different directory and fix the permissions

            mv ./coverage ./naive-coverage
            chmod -R a+w ./naive-coverage

    - Set the coverage data collection granularity to unique count

            export AGENT_GRANULARITY=chain

    - Run the tests

            defects4j test

    - Save the coverage data to a different directory and fix the permissions

            mv ./coverage ./unique-coverage
            chmod -R a+w ./unique-coverage

 3. Calculate the FL-scores/ranks:

    - Enter (python) script directory: 

            cd /python_scripts

    - Run main.py

            python3 -W ignore main.py \
                --naive-folder=[output folder]/naive-coverage/ \
                --naive-mapper=[output folder]/naive-coverage/trace.trc.names \
                --unique-folder=[output folder]/unique-coverage/ \
                --unique-mapper=[output folder]/unique-coverage/trace.trc.names \
                --change=./changed_methods/Lang-changes.csv \
                --bugID=[bug]

        - For example:

                python3 -W ignore main.py \
                    --naive-folder=/sbfl/Lang_1b/naive-coverage/ \
                    --naive-mapper=/sbfl/Lang_1b/naive-coverage/trace.trc.names \
                    --unique-folder=/sbfl/Lang_1b/unique-coverage/ \
                    --unique-mapper=/sbfl/Lang_1b/unique-coverage/trace.trc.names \
                    --change=./changed_methods/Lang-changes.csv \
                    --bugID=1

## Result

Result of python scipt:
| bugID | Barinel| Barinel-C | Jaccard | Jaccard-C | ... |
|--|--|--|--|--|--|
| [ID] | [rank] | [rank] | [rank] | [rank] | [rank] |
  
  - Rank(name):
    - without `-C`: the rank based on "original" (hit)
    - with `-C` : the rank based on call frequency

The `result.csv` contains the average ranks for all bugs.
