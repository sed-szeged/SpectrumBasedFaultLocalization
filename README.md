# Call Frequency-Based Fault Localization

This fault localization concept uses as an additional context the frequency of the investigated method occurring in call stack instances during the course of executing the failing test cases.

## The docker image contains:
 - Defects4J bug dataset [(available)](https://github.com/Frenkymd/defects4j/tree/chain)
 - Java instrumenter [(available)](https://github.com/sed-szeged/java-instrumenter/tree/master)
 - measurements framework [(available)](https://github.com/bvancsics/frequencySBFL/tree/main)

## Steps:

 1. Prepare Docker environment

	- clone this repository
	- build docker:
		 
		    docker build -t sbfl .

 2. Create unique deepest call stacks (UDCS)
	
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

    - Run tests

		    defects4j test

    - Set permissions

		    chmod -R [XXX] ./coverage

		- For example:

			chmod -R 777 ./coverage

 3. Calculate the FL-scores/ranks:

    - Enter (python) script directory: 

		    cd /python_scripts

    - Run main.py

		    python3 -W ignore main.py \
		    	--cov-folder=[output folder]/coverage/ \
		    	--nameMapping=[output folder]/coverage/trace.trc.names \
		    	--change=./changed_methods/Lang-changes.csv \
		    	--bugID=[bug]

		- For example:

			python3 -W ignore main.py \
				--cov-folder=/sbfl/Lang_1b/coverage/ \
				--nameMapping=/sbfl/Lang_1b/coverage/trace.trc.names \
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
