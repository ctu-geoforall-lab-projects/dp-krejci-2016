#!/bin/bash
apt-get install git -y && apt-get clean -y && apt-get autoclean -y && apt-get autoremove -y &&\
rm -rf /var/lib/{apt,dpkg,cache,log}/

wget -q -o out.log -P /tmp http://apache.miloslavbrada.cz/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz && \
tar xzf /tmp/apache-maven-3.3.9-bin.tar.gz -C /usr/local && \
rm /tmp/apache-maven-3.3.9-bin.tar.gz && \
mv /usr/local/apache-maven-3.3.9 /usr/local/maven

export PATH=$PATH:/usr/local/maven/bin

git clone https://github.com/Esri/geometry-api-java.git /usr/local/geometry-api-java  && \
cd /usr/local/geometry-api-java && \
mvn clean install 

git clone https://github.com/Esri/spatial-framework-for-hadoop.git /usr/local/spatial-framework-for-hadoop && \
cd /usr/local/spatial-framework-for-hadoop && \
mvn clean package -DskipTests 

wget -q -o out.log -P /usr/local/ https://github.com/sheetaldolas/Hive-JSON-Serde/archive/json-serde-1.1.9.8.zip && \
unzip /usr/local/json-serde-1.1.9.8.zip -d /usr/local/ && \
rm /usr/local/json-serde-1.1.9.8.zip  

wget -q -o out.log -P /usr/local/ http://spatialhadoop.cs.umn.edu/downloads/spatialhadoop-2.3.tar.gz && \
tar xzf /usr/local/spatialhadoop-2.3.tar.gz -C /usr/local && \
rm /usr/local/spatialhadoop-2.3.tar.gz