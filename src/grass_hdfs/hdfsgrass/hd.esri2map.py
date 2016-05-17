#!/usr/bin/env python
# -*- coding: utf-8 -*-
#%module
#% description:  This module allows to convert esri GeoJson to grass map
#% keyword: database
#% keyword: hdfs
#% keyword: hive
#%end
#%option G_OPT_V_OUTPUT
#% key: out
#% required: yes
#%end
#%option
#% key: path
#% type: string
#% description:  path to the folder with files.
#%end
#%option
#% key: attributes
#% type: string
#% description: list of attributes with datatype
#%end



import os
import sys

import grass.script as grass

from hdfs_grass_lib import GrassMapBuilderEsriToEsri

def main():

    count=0
    files=os.listdir(options['path'])

    for block in files:
        map='%s_0%s'%(options['out'],block)
        block=os.path.join(options['path'],block)
        map_build = GrassMapBuilderEsriToEsri(block,
                                              map,
                                              options['attributes'])
        map_build.build()
        count+=1


if __name__ == "__main__":
    options, flags = grass.parser()
    main()

