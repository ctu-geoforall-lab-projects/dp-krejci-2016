from __future__ import print_function
from __future__ import unicode_literals

import inspect
import logging
import os
import sys
import mmap
path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), os.pardir)
if not path in sys.path:
    sys.path.append(path)

from hdfswrapper.connections import Connection
from hdfswrapper import settings
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Table
from hdfs_grass_util import read_dict, save_dict, get_tmp_folder
from grass.pygrass.modules import Module
from grass.script.core import PIPE
import grass.script as grass
from grass_map  import VectorDBInfo as VectorDBInfoBase

from dagpype import stream_lines, to_stream,filt, nth

class ConnectionManager:
    """
    >>> conn = ConnectionManager()
    >>> conn.set_connection(conn_type='hiveserver2',
    >>>                   conn_id='testhiveconn1',
    >>>                   host='172.17.0.2',
    >>>                   port=10000,
    >>>                   login='root',
    >>>                   password='test',
    >>>                   schema='default')
    >>> conn.drop_connection_table()
    >>> conn.show_connections()
    >>> conn.add_connection()
    >>> conn.test_connection(conn.get_current_Id())
    >>> conn.remove_conn_Id('testhiveconn1')
    >>> print(conn.get_current_Id())
    """

    def __init__(self):

        self.conn_id = None
        self.conn_type = None
        self.host = None
        self.port = None
        self.login = None
        self.password = None
        self.schema = None
        self.authMechanism = None
        self.connected = False
        self.uri = None
        self.connectionDict = None
        self.connection = None

        self.session = settings.Session

    def _connect(self):
        if self.uri:
            self.connectionDict = {'uri': self.uri}
        else:
            self.connectionDict = {'host': self.host}
            if self.login:
                self.connectionDict['login'] = self.login
            if self.schema:
                self.connectionDict['schema'] = self.schema
            if self.conn_id:
                self.connectionDict['conn_id'] = self.conn_id
            if self.conn_type:
                self.connectionDict['conn_type'] = self.conn_type
            if self.password:
                self.connectionDict['password'] = self.password
            if self.port:
                self.connectionDict['port'] = self.port
        self.connection = Connection(**self.connectionDict)

    def add_connection(self):
        print('***' * 30)
        print("\n     Adding new connection \n       conn_type: %s  \n" % self.conn_type)
        self.session.add(self.connection)
        try:
            self.session.commit()
            self._set_active_connection(self.conn_type, self.connectionDict['conn_id'])
        except IntegrityError, e:
            print("       ERROR conn_id already exists. Will be overwritten...\n")
            print('***' * 30)
            self.session.rollback()
            self.session.flush()
            self.remove_conn_Id(self.connectionDict['conn_id'])
            self.add_connection()
            print('***' * 30)

    def set_connection(self, conn_id, conn_type,
                       host=None, port=None,
                       login=None, password=None,
                       schema=None, authMechanism=None):

        if None in [conn_id, conn_type]:
            print("ERROR: no conn_id or conn_type defined")
            return None
        self.conn_id = conn_id
        self.conn_type = conn_type
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.schema = schema
        self.authMechanism = authMechanism

        self._connect()

    @staticmethod
    def drop_connection_table():
        from sqlalchemy import MetaData
        md = MetaData()
        connTable = Table('connection', md)
        try:
            connTable.drop(settings.engine)
            os.remove(settings.grass_config)
            print('***' * 30)
            print("\n     Table of connection has been removed \n")
            print('***' * 30)
        except Exception, e:
            print('***' * 30)
            print("\n     No table exists\n")
            print('***' * 30)

    @staticmethod
    def show_connections():
        cn = settings.engine.connect()
        print('***' * 30)
        print("\n     Table of connection \n")
        try:
            result = cn.execute('select * from connection')
            for row in result:
                print("       %s\n" % row)
            cn.close()
        except Exception, e:
            print(e)
            print("        No connection\n")
        print('***' * 30)

    def set_active_connection(self, conn_type=None, idc=None):
        self.set_connection(conn_type=conn_type, conn_id=idc)
        self._set_active_connection()

    def _set_active_connection(self, conn_type=None, idc=None):
        # print("Saving connection: %s"%settings.grass_config)
        if conn_type is None:
            conn_type = self.conn_type
        if idc is None:
            idc = self.conn_id
        cfg = read_dict(settings.grass_config)
        cfg[conn_type] = idc
        save_dict(settings.grass_config, cfg)

    @staticmethod
    def get_current_Id(conn_type):
        cfg = read_dict(settings.grass_config)
        if cfg:
            if cfg.has_key(conn_type):
                return cfg.get(conn_type)
        else:
            return None

    @staticmethod
    def show_active_connections():
        cfg = read_dict(settings.grass_config)
        if cfg:
            print('***' * 30)
            print('\n     Primary connection for db drivers\n')
            for key, val in cfg.iteritems():
                print('       conn_type: %s -> conn_id: %s\n' % (key, val))
        else:
            print('      No connection defined\n')
        print('***' * 30)

    def get_current_connection(self, conn_type):
        idc = self.get_current_Id(conn_type)
        if idc:
            self.set_connection(conn_id=idc, conn_type=conn_type)
            self._connect()
        else:
            self.connection = None

        return self.connection

    def get_hook(self):
        if self.connection:
            return self.connection.get_hook()
        return None

    @staticmethod
    def remove_conn_Id(id):
        cn = settings.engine.connect()
        print('***' * 30)
        print("\n     Removing connection %s " % id)
        try:
            print('       conn_id= %s \n' % id)
            cn.execute('DELETE FROM connection WHERE conn_id="%s"' % id)
            cn.close()
        except Exception, e:
            print("       ERROR: %s \n" % e)
            # print('     No connection with conn_id %s'%id)
        print('***' * 30)

    def set_connection_uri(self, uri):
        self.uri = uri
        self._connect()

    def test_connection(self, conn_type=None):
        if conn_type is not None:
            self.get_current_connection(conn_type)

        hook = self.get_hook()
        if hook:
            if not hook.test():
                print('Cannot establish connection')
                return False

class HiveTableBuilder:
    def __init__(self,map,layer):
        self.map = map
        self.layer = layer


    def get_structure(self):
        raise NotImplemented
        dtypes=['TINYINT','SMALLINT','INT','BIGINT','BOOLEAN','FLOAT','DOUBLE',
                'STRING','BINARY','TIMESTAMP','DECIMAL','DATE','VARCHAR','CHAR']
        table = VectorDBInfoBase(self.map)
        map_info = table.GetTableDesc(self.map)

        for col in map_info.keys():
            name=str(col)
            dtype=col['type']
            if dtype == 'integet':
                dtype = 'INT'
            if not dtype.capitalize() in dtype:
                grass.fatal('Automatic generation of columns faild, datatype %s is not recognized'%dtype)

    def _get_map(self):
       raise NotImplemented


class JSONBuilder:
    def __init__(self, grass_map=None, json_file=None):

        self.grass_map = grass_map
        self.json_file = json_file
        self.json = ''

    def get_JSON(self):
        if self.grass_map:
            self.json = self._get_grass_json()
        else:
            filename, file_extension = os.path.splitext(self.json_file)
            self.json = os.path.join(get_tmp_folder(), "%s.json" %filename)
        return self.json

    def rm_last_lines(self, path, rm_last_line=3):
        file = open(path, "r+", )

        # Move the pointer (similar to a cursor in a text editor) to the end of the file.
        file.seek(-rm_last_line, os.SEEK_END)

        pos = file.tell() - 1

        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead of this position
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()

        file.close()

    @staticmethod
    def remove_line(filename, lineNumber):
        with open(filename, 'r+') as outputFile:
            with open(filename, 'r') as inputFile:

                currentLineNumber = 0
                while currentLineNumber < lineNumber:
                    inputFile.readline()
                    currentLineNumber += 1

                seekPosition = inputFile.tell()
                outputFile.seek(seekPosition, 0)

                inputFile.readline()

                currentLine = inputFile.readline()
                while currentLine:
                    outputFile.writelines(currentLine)
                    currentLine = inputFile.readline()

            outputFile.truncate()

    def _get_grass_json(self):
        if self.grass_map['type'] not in ['point', 'line', 'boundary', 'centroid',
                                          'area', 'face', 'kernel', 'auto']:
            self.grass_map['type'] = 'auto'
        out = "%s_%s.json" % (self.grass_map['map'],
                              self.grass_map['layer'])

        out = os.path.join(get_tmp_folder(), out)
        if os.path.exists(out):
            os.remove(out)
        out1 = Module('v.out.ogr',
                      input=self.grass_map['map'],
                      layer=self.grass_map['layer'],
                      type=self.grass_map['type'],
                      output=out,
                      format='GeoJSON',
                      stderr_=PIPE,
                      overwrite=True)

        print(out1.outputs["stderr"].value.strip())

        self.rm_last_lines(out, 3)
        # remove first 5 lines and last 3 to enseure format for serializetion
        for i in range(5):  # todo optimize
            self.remove_line(out, 0)

        return out

class GrassMapBuilder:
    def __init__(self, json_file, map):
        self.file = json_file
        self.map = map

    def build(self):
        geom_type = self._get_type()
        self.replace_substring(geom_type[0],[1])
        self.replace_substring('}}}','}}},')

        fst_line= ('{"type": "FeatureCollection","crs": '
                   '{ "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },"features": [')
        self._prepend_line(fst_line)
        self._append_line(']}')

        self._create_map()


    def _get_wkid(self):
        """
        Parse epsg from wkid (esri json)
        :return:
        :rtype:
        """
        f = open('example.txt')
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if s.find('wkid') != -1:
            return self._find_between(s,'wkid":','}')

    def _find_between(self,s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def _create_map(self):
        Module('v.in.ogr',
              dsn=self.file,
              output=self.map,
              stderr_=PIPE,
              overwrite=True)

    def _json_parser(self):
        pass

    def _prepend_line(self,line):
        with open(self.file, "r+") as f:
             old = f.read() # read everything in the file
             f.seek(0) # rewind
             f.write("%s\n"%line + old) # write the new line before

    def _append_line(self,line):
        with open(self.file, 'a') as file:
            file.write(line)

    def _get_type(self):
        line = stream_lines(self.file) | nth(0)
        if line.find('ring'):
            return ['ring','"type":"Polygon","coordinates":']
        if line.find('multipoint'):
            return ['multipoint','"type":"MultiPoint","coordinates":']
        if line.find('paths'):
            return ['paths','"type":"MultiLineString","coordinates":']

        if line.find('"x"'):
            grass.fatal('Point is not supported')
        if line.find('envelope'):
            grass.fatal('Envelope is not supported')

    def replace_substring(self,foo,bar):
        stream_lines(self.file) |\
        filt(lambda l: l.replace(foo, bar)) | \
        to_stream(sys.stdout)



class GrassHdfs():
    def __init__(self, conn_type):
        self.conn = None
        self.hook = None
        self.conn_type = conn_type

        self._init_connection()
        if self.hook is None:
            sys.exit("Connection can not establish")  # TODO

    def _init_connection(self):
        self.conn = ConnectionManager()
        self.conn.get_current_connection(self.conn_type)
        self.hook = self.conn.get_hook()

    @staticmethod
    def printInfo( hdfs, msg=None):
        print('***' * 30)
        if msg:
            print("     %s \n" % msg)
        print(' path :\n    %s\n' % hdfs)
        print('***' * 30)

    def get_path_grass_dataset(self):
        LOCATION_NAME = grass.gisenv()['LOCATION_NAME']
        MAPSET = grass.gisenv()['MAPSET']
        dest_path = os.path.join('grass_data_hdfs', LOCATION_NAME, MAPSET, 'vector')
        self.mkdir(dest_path)
        return dest_path

    def upload(self, fs, hdfs, overwrite=True, parallelism=1):
        logging.info('Trying copy: fs: %s to  hdfs: %s   ' % (fs, hdfs))
        self.hook.upload_file(fs, hdfs, overwrite, parallelism)
        self.printInfo(hdfs, "File has been copied to:")

    def mkdir(self, hdfs):
        self.hook.mkdir(hdfs)
        self.printInfo(hdfs)

    def write(self, hdfs, data, **kwargs):
        # Write file to hdfs
        self.hook.write(hdfs, data, **kwargs)
        self.printInfo(hdfs)

    def download(self, fs, hdfs, overwrite=True, parallelism=1):
        logging.info('Trying download : hdfs: %s to fs: %s   ' % (hdfs, fs))
        out = self.hook.download_file(fs, hdfs, overwrite, parallelism)
        if out:
            self.printInfo(fs, "File has been copied to:")
        else:
            print('Copy error!')
        return out


