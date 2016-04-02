#!/usr/bin/env python
import time
import sys
import psycopg2 as ppg
from datetime import timedelta, datetime
import os
class pgwrapper:
    def __init__(self, dbname='mwdb', host='geo102.fsv.cvut.cz', user='krejcmat', passwd='xx', port=''):
        self.dbname = dbname  # Database name which connect to.
        self.host = host  # Host name (default is "localhost")
        self.user = user  # User name for login to the database.
        self.port = port
        self.password = passwd  # Password for login to the database.
        self.connection = self.setConnect()  # Set a connection to the database
        self.cursor = self.setCursor()  # Generate cursor.

    def setCursor(self):
        try:
            return self.connection.cursor()
        except:
            print 'cannot set cursor'

    def setConnect(self):
        conn_string = "dbname='%s'" % self.dbname
        if self.user:
            conn_string += " user='%s'" % self.user
        if self.host:
            conn_string += " host='%s'" % self.host
        if self.password:
            conn_string += " password='%s'" % self.password
        if self.port:
            conn_string += " port='%s'" % self.port
        try:
            conn = ppg.connect(conn_string)
        except:
            print 'Cannot connect to database'

        return conn
    def copyto(self, afile, table, sep='|'):
        try:
            self.cursor.copy_to(afile, table, sep=sep)
            self.connection.commit()

        except Exception, err:
            self.connection.rollback()
            self.print_message(" Catched error (as expected):\n")
            self.print_message(err)
            pass

    def copyexpert(self, sql, data):
        try:
            self.cursor.copy_expert(sql, data)
        except Exception:
            self.connection.rollback()
            print("ERROR %s"%sql)
            pass

    def executeSql(self, sql, results=True, commit=False):
        # Excute the SQL statement.
        self.print_message (sql)

        try:
            self.cursor.execute(sql)
        except Exception, e:
            self.connection.rollback()
            self.print_message(e.pgerror)

        if commit:
            self.connection.commit()

        if results:
            results = self.cursor.fetchall()
            return results

def main():
    #### YOU CAN EDIT #####
    attributes="linkid, time, txpower, rxpower"
    links="all"
    dateformat="%Y-%m-%d"
    start="2013-12-29"
    end="2014-12-29"
    delta=timedelta(days=10)
    out_file=os.path.dirname(os.path.abspath(__file__))
    out_file='/tmp'
    #### YOU SHOULD NOT EDIT #####
    cur=pgwrapper()
    start_date=datetime.strptime(start,dateformat)
    end_date=datetime.strptime(end,dateformat)
    sql_date_format="%Y-%m-%d"

    try:
        os.mkdir(os.path.join(out_file,'mwdbexport'))
    except:
        pass
    out_file=os.path.join(out_file,'mwdbexport')

    while start_date < end_date:
        start_str=("'%s'")%start_date.strftime(sql_date_format)
        to_TMP=start_date+delta
        to_str_TMP=("'%s'")%to_TMP.strftime(sql_date_format)
        outtime=("%s_%s.csv"%(start_str,to_str_TMP)).replace("'","")

        out=os.path.join(out_file,outtime)
        if links == 'all':
            select="COPY ( SELECT %s FROM record WHERE time >=%s AND time < %s ) TO STDOUT;"%(attributes,start_str,to_str_TMP)
        else:
            select="COPY ( SELECT %s FROM record WHERE linkid IN (%s) and time >=%s AND time < %s ) TO STDOUT;"%(attributes,links,start_str,to_str_TMP)
        print("START \n   %s"%select)

        start = time.time()
        with open(out, 'w') as f:
            cur.copyexpert(select, f)
            f.close()
        print("written to: %s  \n"%out)
        end = time.time()
        print("TIME: %s"%(end - start))
        start_date=to_TMP


if __name__ == '__main__':
    main()
