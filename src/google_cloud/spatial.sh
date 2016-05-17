#!/bin/bash
wget  -P ~/spatial_inst/  http://apache.miloslavbrada.cz/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz
#tar xzf /tmp/apache-maven-3.3.9-bin.tar.gz ~/spatial_inst


git clone https://github.com/Esri/geometry-api-java.git ~/spatial_inst/geometry-api-java
git clone https://github.com/Esri/spatial-framework-for-hadoop.git ~/spatial_inst/spatial-framework-for-hadoop
wget -P ~/spatial_inst/ https://github.com/sheetaldolas/Hive-JSON-Serde/archive/json-serde-1.1.9.8.zip
wget -P ~/spatial_inst/ http://spatialhadoop.cs.umn.edu/downloads/spatialhadoop-2.3.tar.gz
#tar xzf ~/spatial_inst/spatialhadoop-2.3.tar.gz -C ~/spatial_inst/
