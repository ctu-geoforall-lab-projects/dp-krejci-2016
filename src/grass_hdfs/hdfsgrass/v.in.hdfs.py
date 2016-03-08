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
#% key: table
#% type: string
#% required: no
#% description: Name of table for import
#% options: hiveserver2
#% guisection: Connection
#%end

import grass.script as grass
#https://github.com/Esri/gis-tools-for-hadoop/wiki/Getting-the-results-of-a-Hive-query-into-ArcGIS

def main():
    pass

if __name__ == "__main__":
    options, flags = grass.parser()
    main()