FROM hferenc/defects4j

RUN apt-get update && \
	apt-get install -y python3 python3-pip gfortran libopenblas-dev liblapack-dev && \
	pip3 install networkx==2.2

RUN git clone https://github.com/bvancsics/frequencySBFL.git /python_scripts

WORKDIR /sbfl
