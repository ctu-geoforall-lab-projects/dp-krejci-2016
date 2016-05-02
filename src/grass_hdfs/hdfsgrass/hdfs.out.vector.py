#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:       v.out.hdfs
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
#% description: Module for export vector feature to hdfs(JSON)
#% keyword: database
#% keyword: hdfs
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
#% options: webhdfs
#% description: HDFS driver
#%end
#%option G_OPT_V_MAP
#% key: map
#% required: yes
#% label: Name of vector map to export to hdfs
#%end
#%option G_OPT_V_TYPE
#% key: type
#% required: yes
#%end
#%option G_OPT_V_FIELD
#% key: layer
#% required: yes
#%end

import grass.script as grass
from hdfs_grass_lib import JSONBuilder,GRASS2HDFSsnakebite,GRASS2HDFSweb
import os

def main():
    if options['hdfs'] == '@grass_data_hdfs':
        LOCATION_NAME = grass.gisenv()['LOCATION_NAME']
        MAPSET = grass.gisenv()['MAPSET']
        MAPSET_PATH = os.path.join('grass_data_hdfs',LOCATION_NAME,MAPSET,'external')
        options['hdfs'] = MAPSET_PATH
    print options['hdfs']
    grass_map = {"map": options['map'],
                 "layer": options['layer'],
                 "type": options['type'],
                 }
    json = JSONBuilder(grass_map)
    json = json.get_JSON()
    print('cp %s'%json)
   # if options['driver'] == "hdfs":
   #     transf = GRASS2HDFSsnakebite()
   #     transf.cp(json,options['hdfs'])
   #     return

    if options['driver'] == "webhdfs":
        transf = GRASS2HDFSweb()
        transf.cp(json,options['hdfs'])
        return



if __name__ == "__main__":
    options, flags = grass.parser()
    main()

