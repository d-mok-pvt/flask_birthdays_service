FROM openjdk:11-jre-slim

RUN apt-get update && \
    apt-get install -y wget unzip && \
    rm -rf /var/lib/apt/lists/* && \
    wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.21.0/allure-commandline-2.21.0.zip && \
    unzip allure-commandline-2.21.0.zip -d /opt/ && \
    rm allure-commandline-2.21.0.zip && \
    ln -s /opt/allure-2.21.0/bin/allure /usr/bin/allure

WORKDIR /app

CMD ["bash"]
