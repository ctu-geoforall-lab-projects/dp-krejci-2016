#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:       db.hive.execute
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
#% description: Execute HIVEsql command
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
#% options: hive_cli, hiveserver2
#%end
#%option
#% key: hsql
#% type: string
#% required: yes
#% description: hive sql command
#%end
#%option
#% key: schema
#% type: string
#% required: no
#% description: hive db schema
#%end
#%G_OPT_F_OUTPUT
#% key: out
#% type: string
#% required: no
#% description: Name for output file (if omitted output to stdout)
#%end

from hdfs_grass_lib import ConnectionManager
import grass.script as grass


def main():
    conn=ConnectionManager()

    conn.getCurrentConnection(options["conn_type"])
    hive = conn.getHook()

    if not options['schema']:
        options['schema']='default'

    out = hive.get_results(hql=options['hsql'],
                     schema=options['schema'])

    if options['out']:
        with open(out,'rw') as io:
            io.writelines(out)
            io.close()
    else:
        print out

if __name__ == "__main__":
    options, flags = grass.parser()
    main()
