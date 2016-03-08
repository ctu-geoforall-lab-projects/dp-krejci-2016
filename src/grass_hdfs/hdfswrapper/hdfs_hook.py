from hdfswrapper.base_hook import BaseHook

try:
    snakebite_imported = True
    from snakebite.client import Client, HAClient, Namenode
except ImportError:
    snakebite_imported = False



class HDFSHookException(Exception):
    pass


class HDFSHook(BaseHook):
    '''
    Interact with HDFS. This class is a wrapper around the snakebite library.
    '''
    def __init__(self, hdfs_conn_id='hdfs_default', proxy_user=None):
        if not snakebite_imported:
            raise ImportError(
                'This HDFSHook implementation requires snakebite, but '
                'snakebite is not compatible with Python 3 '
                '(as of August 2015). Please use Python 2 if you require '
                'this hook  -- or help by submitting a PR!')
        self.hdfs_conn_id = hdfs_conn_id
        self.proxy_user = proxy_user

    def get_conn(self):
        '''
        Returns a snakebite HDFSClient object.
        '''
        use_sasl = False
        securityConfig=None
        if securityConfig == 'kerberos': #TODO make confugration file for thiw
            use_sasl = True

        connections = self.get_connections(self.hdfs_conn_id)
        client = None
        #When using HAClient, proxy_user must be the same, so is ok to always take the first
	effective_user = self.proxy_user or connections[0].login
        if len(connections) == 1:
            client = Client(connections[0].host, connections[0].port, use_sasl=use_sasl, effective_user=effective_user)
        elif len(connections) > 1:
            nn = [Namenode(conn.host, conn.port) for conn in connections]
            client = HAClient(nn, use_sasl=use_sasl, effective_user=effective_user)
        else:
            raise HDFSHookException("conn_id doesn't exist in the repository")
        return client

    def test(self):
        try:
            client = self.get_conn()
            print("\n-----Test connection (ls /) -----")
            print(type(client.count(['/'])))
            print('-'*40 +'\n')
            return False
        except Exception, e:
            print("     EROOR: connection can not be established: %s" % e)
            print('-'*40 +'\n')
            return False
    def get_cursor(self):
        NotImplementedError()

    def execute(self,hql):
        NotImplementedError()