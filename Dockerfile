FROM openjdk:7-jdk-jessie

ARG AGENT_VERSION

RUN apt-get update && \
    apt-get install -y build-essential maven && \
    curl -L https://cpanmin.us | perl - App::cpanminus

RUN apt-get install -y python3 python3-pip gfortran libopenblas-dev liblapack-dev
RUN pip3 install networkx==2.2



RUN git clone https://github.com/bvancsics/frequencySBFL.git /python_scripts
	


RUN git clone https://github.com/Frenkymd/defects4j.git /defects4j
WORKDIR /defects4j
RUN git checkout chain
RUN cpanm --installdeps . && ./init.sh
ENV PATH="/defects4j/framework/bin:${PATH}"
WORKDIR /


RUN git clone https://github.com/sed-szeged/java-instrumenter.git /instrumenter
WORKDIR /instrumenter
RUN mvn clean package
RUN cp /instrumenter/target/method-agent-$AGENT_VERSION-jar-with-dependencies.jar /defects4j/framework/lib/agent.jar
