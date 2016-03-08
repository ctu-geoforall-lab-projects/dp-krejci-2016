#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:       v.hdfs.hive.table
# AUTHOR(S):    Matej Krejci (matejkrejci@gmail.com
#
# PURPOSE:      Reproject the entire mapset
# COPYRIGHT:    (C) 2016 by the GRASS Development Team
#
#               This program is free software under the GNU General
#               Public License (>=v2). Read the file COPYING that
#               comes with GRASS for details.
#
#############################################################################

#%module
#% description: Creating spatial tables based on ESRI spatial framework
#% keyword: database
#% keyword: hdfs
#% keyword: hive
#%end

#%option
#% key: conn_type
#% type: string
#% required: yes
#% answer: hiveserver2
#% description: Type of database driver
#% options: hive_cli,hiveserver2
#% guisection: table
#%end
#%option
#% key: table
#% type: string
#% required: yes
#% description: name of table
#% guisection: table
#%end
#%option
#% key: attributes
#% type: string
#% required: yes
#% description: python dictionary {attribute:datatype}
#% guisection: table
#%end
#%flag
#% key: e
#% description: The EXTERNAL keyword lets you create a table and provide a LOCATION so that Hive does not use a default location for this table. This comes in handy if you already have data generated. When dropping an EXTERNAL table, data in the table is NOT deleted from the file system.
#% guisection: table
#%end
#%option
#% key: jsonformat
#% type: string
#% required: yes
#% answer: enclosed
#% description: Enclosed is GRASS default
#% options: enclosed, unenclosed
#% guisection: table
#%end
#%option
#% key: serde
#% type: string
#% required: yes
#% answer: com.esri.hadoop.hive.serde.JsonSerde
#% description: java class for serialization of json
#% guisection: table
#%end
#%option
#% key: outformat
#% type: string
#% required: yes
#% answer: org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat
#% description: java class for handling output format
#% guisection: table
#%end
#%option
#% key: jsonpath
#% type: string
#% required: yes
#% description: hdfs path specifying input data
#% guisection: data
#%end
#%flag
#% key: o
#% description: Possible if filepath for loading data is delcared. True-overwrite all data in table.
#% guisection: data
#%end
#%flag
#% key: d
#% description: Firstly drop table if exists
#% guisection: table
#%end

from hdfs_grass_lib import ConnectionManager
import grass.script as grass


def main():

    conn=ConnectionManager()
    conn.getCurrentConnection(options["conn_type"])
    hive = conn.getHook()
    hive.create_geom_table( table=options['table'],
                            field_dict=options['attributes'],
                            serde=options['serde'],
                            inputformat=options['jsonformat'],
                            outputformat=options['outformat'],
                            external=flags['e'],
                            recreate=flags['d'],
                            filepath=options['jsonpath'],
                            overwrite=flags['o'])

if __name__ == "__main__":
    options, flags = grass.parser()
    main()







