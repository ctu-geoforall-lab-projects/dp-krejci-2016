#!/bin/bash

#path to buckets with desired instalation
ins_path=gs://init_hadoop/
#rm -fr $ins_path
#sudo mkdir $ins_path

#gsutil -m -o GSUtil:parallel_composite_upload_threshold=150M cp -r gs://init_hadoop/* $ins_path



tar xzf $ins_path/apache-maven-3.3.9-bin.tar.gz -C $ins_path
mv -f $ins_path/apache-maven-3.3.9 $ins_path/maven
#rm -fr $ins_path/apache-maven-3.3.9

export  PATH="$PATH:$ins_path/maven/bin"

#RUN git clone https://github.com/Esri/geometry-api-java.git $ins_path/geometry-api-java
cd $ins_path/geometry-api-java
mvn clean install 

#git clone https://github.com/Esri/spatial-framework-for-hadoop.git $ins_path/spatial-framework-for-hadoop
cd $ins_path/spatial-framework-for-hadoop
mvn clean package -DskipTests 

#RUN wget -q -o out.log -P $ins_path https://github.com/sheetaldolas/Hive-JSON-Serde/archive/json-serde-1.1.9.8.zip
unzip $ins_path/json-serde-1.1.9.8.zip -d $ins_path
#rm $ins_path/json-serde-1.1.9.8.zip

#RUN wget -q -o out.log -P $ins_path/ http://spatialhadoop.cs.umn.edu/downloads/spatialhadoop-2.3.tar.gz
tar xzf $ins_path/spatialhadoop-2.3.tar.gz -C $ins_path
#rm $ins_path/spatialhadoop-2.3.tar.gz
