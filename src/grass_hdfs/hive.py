from hdfswrapper.hive_hook import HiveServer2Hook
from hdfswrapper.connections import Connection
from hdfswrapper import settings
from sqlalchemy.exc import IntegrityError

import os,sys

conn_id='hiveserver2_default'
conn_type='hiveserver2'
host='172.17.0.2'
login='root'
password='test'
schema='default'
port=10000


conn=Connection(conn_id='hiveserver2_default',conn_type='hiveserver2' )
# conn=Connection(conn_id,
#                 conn_type,host,
#                 login,password,schema,port)
# conn.set_password('test')
# session=settings.Session
# session.add(conn)
# try:
#     session.commit()
# except IntegrityError,e:
#     print(e)
#     session.rollback()
#     session.flush()

hook = conn.get_hook()
cur=hook.get_cursor()
sys.exit()
sql='show databases'
cur.execute(str(sql))
res = cur.fetch()
print(res)


# hk=conn.get_hook()
# sql="show tables"
# #gcn=hk.get_conn()
# gcn=len(hk.get_records(sql))
