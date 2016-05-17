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
#% description: Module for creting map from HIVE table. This module allows to convert esri GeoJson to grass map
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
#%option G_OPT_V_OUTPUT
#% key: out
#% required: yes
#%end
#%flag
#% key: r
#% description: remove temporal file
#% guisection: data
#%end
#%option
#% key: attributes
#% type: string
#% description: list of attributes with datatype
#% guisection: data
#%end

import os
import sys

import grass.script as grass

from hdfs_grass_lib import GrassMapBuilderEsriToEsri, GrassHdfs, ConnectionManager
from hdfs_grass_util import get_tmp_folder


# https://github.com/Esri/gis-tools-for-hadoop/wiki/Getting-the-results-of-a-Hive-query-into-ArcGIS
import shutil

def main():
    tmp_dir = os.path.join(get_tmp_folder(), options['out'])

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    transf = GrassHdfs(options['driver'])
    table_path = options['hdfs']

    if options['table']:
        conn = ConnectionManager()
        conn.get_current_connection('hiveserver2')

        if not conn.get_current_connection('hiveserver2'):
            grass.fatal("Cannot connet to hive for table description. "
                        "Use param hdfs without param table")

        hive = conn.get_hook()
        #table_path = hive.find_table_location(options['table'])
        #tmp_tbl_dir = os.path.join(tmp_dir,options['table'])
    #else:
        #table_name_from_hdfs_path=os.path.basename(os.path.normpath(options['hdfs']))
        #tmp_tbl_dir = os.path.join(tmp_dir,table_name_from_hdfs_path)


    #if not os.path.exists(tmp_tbl_dir):
    #    os.mkdir(tmp_tbl_dir)

    if not transf.download(hdfs=table_path,
                           fs=tmp_dir):
        return


    count=0
    files=os.listdir(tmp_dir)

    for block in files:
        block=os.path.join(tmp_dir,block)
        map_build = GrassMapBuilderEsriToEsri(block,
                                              '%s_0%s'%(options['out'],str(count)),
                                              options['attributes'])
        try:
            map_build.build()
        except Exception ,e:
            grass.warning("Error: %s\n     Map < %s >  conversion failed"%(e,block))
        count+=1




if __name__ == "__main__":
    options, flags = grass.parser()
    main()
