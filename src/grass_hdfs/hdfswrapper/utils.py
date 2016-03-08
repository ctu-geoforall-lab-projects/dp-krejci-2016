from tempfile import mkdtemp
import shutil
import errno
import os
import imp
import logging
try:
    from cryptography.fernet import Fernet
except:
    pass

def TemporaryDirectory(suffix='', prefix=None, dir=None):
    name = mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
    try:
        yield name
    finally:
            try:
                shutil.rmtree(name)
            except OSError as e:
                # ENOENT - no such file or directory
                if e.errno != errno.ENOENT:
                    raise e


def import_module_attrs(parent_module_globals, module_attrs_dict):
    '''
    Attempts to import a set of modules and specified attributes in the
    form of a dictionary. The attributes are copied in the parent module's
    namespace. The function returns a list of attributes names that can be
    affected to __all__.
    This is used in the context of ``operators`` and ``hooks`` and
    silence the import errors for when libraries are missing. It makes
    for a clean package abstracting the underlying modules and only
    brings functional operators to those namespaces.
    '''
    imported_attrs = []
    for mod, attrs in list(module_attrs_dict.items()):
        try:
            path = os.path.realpath(parent_module_globals['__file__'])
            folder = os.path.dirname(path)
            f, filename, description = imp.find_module(mod, [folder])
            module = imp.load_module(mod, f, filename, description)
            for attr in attrs:
                parent_module_globals[attr] = getattr(module, attr)
                imported_attrs += [attr]
        except Exception as err:
            logging.debug("Error importing module {mod}: {err}".format(
                mod=mod, err=err))
    return imported_attrs

def generate_fernet_key():
    try:
        FERNET_KEY = Fernet.generate_key().decode()
    except NameError:
        FERNET_KEY = "cryptography_not_found_storing_passwords_in_plain_text"
    return FERNET_KEY


def string2dict(string):
    try:
        return eval(string)
    except Exception,e:
        print('Dictonary is not valid: %s'%e)
        return None



def findSTfnc(hsql):
        '''
        Parse hsql query and find ST_ functions.
        :param hsql: string of hive query.
        :type hsql: string
        :return: dict {ST_fce: com.esri.hadoop.hive.ST_fce} (name: java path )
        :rtype: dict
        '''
        first = "ST_"
        last = "("
        ST={}
        for s in hsql.split('('):
            if s.find('ST_'):
                s = s.split('ST_')
                fc = 'ST_%s'%s[0]
                if not fc in ST:
                    ST[s]="com.esri.hadoop.hive.%s"%fc

        return ST
