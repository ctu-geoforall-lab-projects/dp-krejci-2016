#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:       db.hive.connect
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
#% description: Connection manager for Hive database
#% keyword: database
#% keyword: hdfs
#%end
#%option
#% key: conn_type
#% type: string
#% required: no
#% description: Type of database driver
#% options: hiveserver2, hdfs, webhdfs, jdbc
#% guisection: Connection
#%end
#%option
#% key: conn_id
#% type: string
#% required: no
#% description: Identificator of connection(free string)
#% guisection: Connection
#%end
#%option
#% key: host
#% description: host
#% type: string
#% required: no
#% guisection: Connection
#%end
#%option
#% key: port
#% type: integer
#% required: no
#% description: Port of db
#% guisection: Connection
#%end
#%option
#% key: login
#% type: string
#% required: no
#% description: Login
#% guisection: Connection
#%end
#%option
#% key: passwd
#% type: string
#% required: no
#% description: Password
#% guisection: Connection
#%end
#%option
#% key: schema
#% type: string
#% required: no
#% description: schema
#% guisection: Connection
#%end
#%option
#% key: authmechanism
#% type: string
#% required: no
#% options: PLAIN
#% description: Authentification mechanism type
#% guisection: Connection
#%end
#%option
#% key: connectionuri
#% type: string
#% required: no
#% description: connection uri string of database
#% guisection: Connection uri
#%end
#%option
#% key: rmid
#% type: integer
#% required: no
#% description: Remove connection by id
#% guisection: manager
#%end
#%flag
#% key: c
#% description: Print table of connection
#% guisection: manager
#%end
#%flag
#% key: p
#% description: Print active connection
#% guisection: manager
#%end
#%flag
#% key: r
#% description: Remove all connections
#% guisection: manager
#%end
#%flag
#% key: t
#% description: Test connection by conn_type
#% guisection: manager
#%end
#%flag
#% key: a
#% description: Set active connection by conn_id and conn_type
#% guisection: manager
#%end

import grass.script as grass
from hdfs_grass_lib import ConnectionManager

def main():
    #add new connection
    conn = ConnectionManager()
    if options['connectionuri']:
        conn.setConnectionURI(options['connectionuri'])
        conn.addNewConnection()
        conn.testConnection()
        return

    if options['host'] and options['conn_type'] and options['conn_id']:
        conn.setConenction(conn_type=options['conn_type'],
                          conn_id=options['conn_id'],
                          host=options['host'],
                          port=options['port'],
                          login=options['login'],
                          password=options['passwd'],
                          schema=options['schema']
                          )
        conn.addNewConnection()
        conn.testConnection()
        return

    if options['rmid']:
        conn.removeConnById(options['rmid'])
        return
    #print table of connection
    elif flags['c']:
        conn.showConnections()
        return
    #drop table with connections
    elif flags['r']:
        conn.dropConnectionTable()
        conn.showConnections()
        return
    #print active connection
    elif flags['p']:
        conn.showActiveConnections()
        return
    elif flags['t']:
        if options['conn_type']:
            conn.testConnection(options['conn_type'])
        else:
            print('conn_type is not set')
        return
    elif flags['a']:
        if not options['conn_type'] and options['conn_id']:
            conn.setActiveConnection(options['conn_type'] ,options['conn_id'])
        else:
            print("ERROR parameter 'conn_type' and 'conn_id' must be set")

if __name__ == "__main__":
    options, flags = grass.parser()
    main()
