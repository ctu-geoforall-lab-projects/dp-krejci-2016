
create function ST_AsGeoJSON as  'com.esri.hadoop.hive.ST_AsGeoJson';
create function ST_GeomFromGeoJSON as  'com.esri.hadoop.hive.ST_GeomFromGeoJson';

CREATE TABLE census_text (
type string,
properties map<string,string>,
geometry string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
STORED AS TEXTFILE;
 
LOAD DATA INPATH '/tmp/2010_census.json' OVERWRITE INTO TABLE  census_text;


DROP TABLE cansus_enc;
CREATE TABLE cansus_enc(area binary, count string)
ROW FORMAT SERDE 'com.esri.hadoop.hive.serde.JsonSerde'              
STORED AS INPUTFORMAT 'com.esri.json.hadoop.EnclosedJsonInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat';

DROP TABLE cansus_unenc;
CREATE TABLE cansus_unenc(area binary, count string)
ROW FORMAT SERDE 'com.esri.hadoop.hive.serde.JsonSerde'              
STORED AS INPUTFORMAT 'com.esri.json.hadoop.UnenclosedJsonInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat';


INSERT OVERWRITE TABLE cansus_enc select ST_GeomFromGeoJSON(geometry),type from census_text where geometry != 'NULL';
INSERT OVERWRITE TABLE cansus_unenc select ST_GeomFromGeoJSON(geometry),type from census_text where geometry != 'NULL';



INSERT OVERWRITE TABLE cansus_enc select ST_GeomFromGeoJSON(geometry),type from census_orc;
INSERT OVERWRITE TABLE cansus_unenc select ST_GeomFromGeoJSON(geometry),type from census_orc;


146.148.23.94 cluster-2-m.c.spatial-hadoop.internal cluster-2-m
23.251.132.118 cluster-2-w-0.c.spatial-hadoop.internal cluster-2-w-0
130.211.67.156 cluster-2-w-1.c.spatial-hadoop.internal cluster-2-w-1
