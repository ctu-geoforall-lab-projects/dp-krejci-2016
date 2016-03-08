#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:       db.hive.table
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
#% description: Hive table creator
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
#% options: hiveserver2, hiveserver2
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
#%option
#% key: external
#% type: bool
#% required: yes
#% description: the EXTERNAL keyword lets you create a table and provide a LOCATION so that Hive does not use a default location for this table. This comes in handy if you already have data generated. When dropping an EXTERNAL table, data in the table is NOT deleted from the file system.
#% guisection: table
#%end
#%option
#% key: outputformat
#% type: string
#% required: yes
#% answer: org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat
#% description: java class for handling output format
#% guisection: table
#%end
#%option
#% key: csvpath
#% type: string
#% required: no
#% description: hdfs path specifying input data
#% guisection: data
#%end
#%option
#% key: partition
#% type: string
#% required: no
#% description: arget partition as a dict of partition columns and values
#% guisection: data
#%end
#%option
#% key: delimeter
#% type: string
#% required: yes
#% answer: ,
#% description: csv delimeter of fields
#% guisection: data
#%end
#%flag
#% key: o
#% description: Optional if csvpath for loading data is delcared. overwrite all data in table.
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
    hive.create_csv_table(table=options['table'],
                          field_dict=options['attributes'],
                          partition=options['partition'],
                          delimiter=options['delimiter'],
                          external=flags['e'],
                          recreate=flags['d'],
                          filepath=options['jsonpath'],
                          overwrite=flags['o'])

if __name__ == "__main__":
    options, flags = grass.parser()
    main()
