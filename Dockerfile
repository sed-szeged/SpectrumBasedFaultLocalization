FROM hferenc/defects4j

RUN apt-get update && \
	apt-get install -y python3 python3-pip gfortran libopenblas-dev liblapack-dev && \
	pip3 install decorator==4.3.0 networkx==2.2 && \
	pip3 install numpy==1.14.4 && \
	pip3 install scipy==1.1.0

RUN git clone https://github.com/bvancsics/frequencySBFL.git /python_scripts
RUN cd /python_scripts && git checkout hit-naive-unique-spectras

WORKDIR /sbfl
