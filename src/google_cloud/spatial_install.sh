#!/bin/bash

sudo apt-get update
sudo apt-get install -y maven  default-jdk git mc



ins_path=/usr/local/spatial
jar_path=/usr/lib/hive/auxlib/
sudo rm -fr  $ins_path
sudo mkdir $ins_path
sudo mkdir $jar_path

cd $ins_path

#sudo gsutil -m -o GSUtil:parallel_composite_upload_threshold=150M cp -r gs://init_hadoop/* $ins_path

sudo git clone https://github.com/Esri/geometry-api-java.git
cd geometry-api-java
sudo mvn clean install 
cd $ins_path


sudo git clone https://github.com/Esri/spatial-framework-for-hadoop.git
cd spatial-framework-for-hadoop
sudo mvn clean package -DskipTests 
cd $ins_path


sudo git clone https://github.com/rcongiu/Hive-JSON-Serde.git
cd Hive-JSON-Serde  
#for hadoop2.x  https://github.com/rcongiu/Hive-JSON-Serde#compile
sudo mvn -Phdp23 clean package 
#for hadoop 1.x
#sudo mvn -Pcdh4 clean package
cd $ins_path

sudo mkdir spatialhadoop
cd spatialhadoop
sudo wget http://spatialhadoop.cs.umn.edu/downloads/spatialhadoop-2.3.tar.gz
sudo tar xzf spatialhadoop-2.3.tar.gz 
#rm $ins_path/spatialhadoop-2.3.tar.gz

cd $jar_path
echo pwd $jar_path
pwd



sudo cp ${ins_path}/Hive-JSON-Serde/json-serde/target/json-serde-1.3.8-SNAPSHOT-jar-with-dependencies.jar $jar_path
sudo cp ${ins_path}/geometry-api-java/target/esri-geometry-api-1.2.1.jar $jar_path
sudo cp ${ins_path}/spatial-framework-for-hadoop/hive/target/spatial-sdk-hive-1.1.1-SNAPSHOT.jar $jar_path
sudo cp ${ins_path}/spatial-framework-for-hadoop/json/target/spatial-sdk-json-1.1.1-SNAPSHOT.jar $jar_path

/usr/lib/hive/auxlib/spatial-framework-for-hadoop/json/target/spatial-sdk-json-1.1.1-SNAPSHOT.jar 
/usr/lib/hive/auxlib/spatial-framework-for-hadoop/hive/target/spatial-sdk-hive-1.1.1-SNAPSHOT.jar 
/usr/lib/hive/auxlib/Hive-JSON-Serde/json-serde/target/json-serde-1.3.8-SNAPSHOT-jar-with-dependencies.jar
/usr/lib/hive/auxlib/geometry-api-java/target/esri-geometry-api-1.2.1.jar


/usr/lib/hive/auxlib/spatial-framework-for-hadoop/json/target/spatial-sdk-json-1.1.1-SNAPSHOT.jar,/usr/lib/hive/auxlib/spatial-framework-for-hadoop/hive/target/spatial-sdk-hive-1.1.1-SNAPSHOT.jar,/usr/lib/hive/auxlib/Hive-JSON-Serde/json-serde/target/json-serde-1.3.8-SNAPSHOT-jar-with-dependencies.jar,/usr/lib/hive/auxlib/geometry-api-java/target/esri-geometry-api-1.2.1.jar
#add path with jars and restart hive
#<property>
#<name>hive.aux.jars.path</name>
#<value>/var/lib/hive</value>
#</property>
#/etc/hadoop/conf.empty/hadoop-env.sh
#export HIVE_AUX_JARS_PATH=/usr/local/spatial/jar
#sudo hiveserver2 restart


#<property>
#<name>hive.aux.jars.path</name>
#<value>/usr/lib/hive/auxlib/spatial-sdk-json-1.1.1-SNAPSHOT.jar,/usr/lib/hive/auxlib/spatial-sdk-hive-1.1.1-SNAPSHOT.jar,/usr/lib/hive/auxlib/json-serde-1.3.8-SNAPSHOT-jar-with-dependencies.jar,/usr/lib/hive/auxlib/esri-geometry-api-1.2.1.jar</value>
#</property>