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

# %module
# % description: Module for creting map from HIVE geometry table
# % keyword: database
# % keyword: hdfs
# % keyword: hive
# %end
# % key: driver
# % type: string
# % required: yes
# % options: webhdfs
# % description: HDFS driver
# %end
# %option
# % key: table
# % type: string
# % required: yes
# % description: Name of table for import
# %end
# % key: out
# % type: string
# % required: yes
# % description: Name of output map
# %end
# %flag
# % key: r
# % description: remove temporal file
# % guisection: data
# %end

import os

import grass.script as grass

from hdfs_grass_lib import GrassMapBuilder, GrassHdfs, ConnectionManager
from hdfs_grass_util import get_tmp_folder


# https://github.com/Esri/gis-tools-for-hadoop/wiki/Getting-the-results-of-a-Hive-query-into-ArcGIS

def main():
    tmp_file = os.path.join(get_tmp_folder(), options['out'])

    conn = ConnectionManager()
    conn.get_current_connection(options["driver"])
    transf = GrassHdfs(options['driver'])

    if not transf.download(hdfs=options['hdfs'],
                           fs=tmp_file,
                           overwrite=flags['r']):
        return

    map_build = GrassMapBuilder(tmp_file, options['out'])


if __name__ == "__main__":
    options, flags = grass.parser()
    main()
