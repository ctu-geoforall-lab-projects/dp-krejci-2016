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

# %module
# % description: Module for export vector feature to hdfs(unenclosed JSON)
# % keyword: database
# % keyword: hdfs
# % keyword: hive
# %end
# %option
# % key: hdfs
# % type: string
# % answer: @grass_data_hdfs
# % required: yes
# % description: HDFS path or default grass dataset
# %end
# %option
# % key: driver
# % type: string
# % required: yes
# % options: hdfs,webhdfs
# % description: HDFS driver
# %end
# %option G_OPT_F_INPUT
# % key: file
# % guisection: fileinput
# %end


import os

import grass.script as grass

from hdfs_grass_lib import GrassHdfs


def main():
    if options['hdfs'] == '@grass_data_hdfs':
        LOCATION_NAME = grass.gisenv()['LOCATION_NAME']
        MAPSET = grass.gisenv()['MAPSET']
        MAPSET_PATH = os.path.join('grass_data_hdfs', LOCATION_NAME, MAPSET, 'external')
        options['hdfs'] = MAPSET_PATH
    print options['hdfs']

    if options['fileinput']:
        transf = GrassHdfs(options['driver'])
        transf.upload(options['fileinput'], options['hdfs'])


if __name__ == "__main__":
    options, flags = grass.parser()
    main()
