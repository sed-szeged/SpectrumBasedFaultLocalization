# Call Frequency-Based Fault Localization


## The docker image contains:
 - Defects4J bug dataset [(available)](https://github.com/Frenkymd/defects4j/tree/chain)
 - Java instrumenter [(available)](https://github.com/sed-szeged/java-instrumenter/tree/master)
 - measurements framework [(available)](https://github.com/bvancsics/frequencySBFL/tree/main)

## Steps:

 1. Start Docker

	- clone this repository
	- build docker:
		 
		    docker build -t d4j --build-arg AGENT_VERSION=0.0.4 .

 2. Create unique deepest call stacks (UDCS)

    - Docker image-id: 
    
		    docker image ls
	
	- Start docker
		 
		    docker run -i -t [IMAGE ID]
		- For example: docker run -i -t 25a0b0ce79a0 /bin/bash

   - [Docker is running...]

	- Download a Defects4J-bug

		    defects4j checkout -p [project] -v [bug][version] -w [output folder]
		- For example: defects4j checkout -p Lang -v 1b -w /defects4j/Lang_1b

	- Enter bug's directory

		    cd [output folder]
      - For example: cd /defects4j/Lang_1b

	- Compile project

		    defects4j compile

	- Run tests

		    defects4j test

	- Set permissions

		    chmod -R [XXX] ./coverage
      - For example:  chmod -R 777 ./coverage

 2. Calculate the FL-scores/ranks:

    - Enter (python) script directory: 

		    cd /python_scripts

	- Run main.py

		    python3 -W ignore main.py --cov-folder=[output folder]/coverage/ --nameMapping=[output folder]/coverage/trace.trc.names --change=./changed_methods/Lang-changes.csv --bugID=[bug]
      - For example:  python3 -W ignore main.py --cov-folder=/defects4j/Lang_1b/coverage/ --nameMapping=/defects4j/Lang_1b/coverage/trace.trc.names --change=./changed_methods/Lang-changes.csv --bugID=1

## Result

Result of python scipt:
| bugID | Barinel| Barinel-C | Jaccard | Jaccard-C | ... |
|--|--|--|--|--|--|
| [ID] | [rank] | [rank] | [rank] | [rank] | [rank] |
  
  - Rank(name):
    - without `-C`: the rank based on "original" (hit)
    - with `-C` : the rank based on call frequency

The `result.csv` contains the average ranks for all bugs.
