#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:       hdfs.copy
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
#% description: Module for export vector feature to hdfs(unenclosed JSON)
#% keyword: database
#% keyword: hdfs
#% keyword: hive
#%end
#%option
#% key: hdfs
#% type: string
#% answer: @grass_data_hdfs
#% required: yes
#% description: HDFS path or default grass dataset
#%end
#%option
#% key: driver
#% type: string
#% required: yes
#% options: hdfs,webhdfs
#% description: HDFS driver
#%end
#%option G_OPT_F_INPUT
#% key: jsoninput
#% guisection: json
#%end
#%option
#% key: jsontype
#% type: string
#% options: enclosed, unenclosed
#% description: Select type of input JSON
#% guisection: json
#%end
#%option G_OPT_F_INPUT
#% key: csv
#% guisection: csv
#%end


import grass.script as grass
from hdfs_grass_lib import JSONBuilder,GRASS2HDFSsnakebite,GRASS2HDFSweb
import os

def main():
    localfile = None
    if options['hdfs'] == '@grass_data_hdfs':
        LOCATION_NAME = grass.gisenv()['LOCATION_NAME']
        MAPSET = grass.gisenv()['MAPSET']
        MAPSET_PATH = os.path.join('grass_data_hdfs',LOCATION_NAME,MAPSET,'external')
        options['hdfs'] = MAPSET_PATH
    print options['hdfs']

    if options['jsoninput']:
        if not options['jsontype']:
            print("ERROR: set json input type")
        json = JSONBuilder(json_file=options['jsoninput'],json_type=options['jsontype'])
        localfile = json.get_JSON()

    if options['csv']:
        localfile=options['csv']

    if localfile:
        if options['driver'] == "hdfs":
            transf = GRASS2HDFSsnakebite()
            transf.cp(localfile,options['hdfs'])

        if options['driver'] == "webhdfs":
            transf = GRASS2HDFSweb()
            transf.cp(localfile,options['hdfs'])

if __name__ == "__main__":
    options, flags = grass.parser()
    main()

