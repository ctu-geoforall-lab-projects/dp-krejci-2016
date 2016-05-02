#!/bin/bash


while true
do
	sudo apt-get update
	if [ $? -eq 0 ];then
	    sudo apt-get install -y maven  default-jdk git 
	    break
	else
	    sleep 10
	fi
done


ins_path=/usr/local/spatial

sudo rm -fr  $ins_path
sudo mkdir $ins_path
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
sudo mvn -Pcdh4 clean package
cd $ins_path

sudo mkdir spatialhadoop
cd spatialhadoop
sudo wget http://spatialhadoop.cs.umn.edu/downloads/spatialhadoop-2.3.tar.gz
sudo tar xzf spatialhadoop-2.3.tar.gz 
#rm $ins_path/spatialhadoop-2.3.tar.gz
cd ~
pwd