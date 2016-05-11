#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:       v.in.hive
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
#% description: Module for creting map from HIVE geometry table
#% keyword: database
#% keyword: hdfs
#% keyword: hive
#%end
#%option
#% key: driver
#% type: string
#% required: yes
#% options: webhdfs
#% description: HDFS driver
#%end
#%option
#% key: table
#% type: string
#% description: Name of table for import
#%end
#%option
#% key: hdfs
#% type: string
#% description: Hdfs path to the table. See hive.info table -h
#%end
#%option
#% key: out
#% type: string
#% required: yes
#% description: Name of output map
#%end
#%flag
#% key: r
#% description: remove temporal file
#% guisection: data
#%end

import os
import sys

import grass.script as grass

from hdfs_grass_lib import GrassMapBuilderEsriToEsri, GrassHdfs, ConnectionManager
from hdfs_grass_util import get_tmp_folder


# https://github.com/Esri/gis-tools-for-hadoop/wiki/Getting-the-results-of-a-Hive-query-into-ArcGIS

def main():
    tmp_dir = os.path.join(get_tmp_folder(), options['out'])
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)


    table_path = options['hdfs']

    if options['table']:
        conn = ConnectionManager()
        conn.get_current_connection('hiveserver2')

        if not conn.get_current_connection('hiveserver2'):
            grass.fatal("Cannot connet to hive for table description. "
                        "Use param hdfs without param table")

        hive = conn.get_hook()
        table_path = hive.find_table_location(options['table'])
        tmp_path = os.path.join(tmp_dir,options['table']+'.json')
    else:
        tmp_path = os.path.join(tmp_dir,'000000_0.json')

    table_path = os.path.join(table_path,'000000_0')


    transf = GrassHdfs(options['driver'])
    if not transf.download(hdfs=table_path,
                           fs=tmp_path):
        return




    map_build = GrassMapBuilderEsriToEsri(tmp_path, options['out'])
    map_build.build()


if __name__ == "__main__":
    options, flags = grass.parser()
    main()
