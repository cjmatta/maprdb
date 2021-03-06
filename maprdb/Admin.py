from ctypes import *
from Connection import Connection

try:
    maprclient = CDLL("/opt/mapr/lib/libMapRClient.dylib.1")
except Exception, e:
    raise e


class hb_admin_disconnection_cb(Structure):
    _fields_ = [
        ('err', c_int32),
        ('admin', c_void_p),
        ('extra', c_void_p)
    ]


class Admin(object):
    def __init__(self, connection=None):
        self._admin = c_void_p()
        self.connection = connection

        if self.connection is None:
            self.connection = Connection()

        if self._admin.value is None:
            self.admin_create()

    def admin_create(self):
        maprclient.hb_admin_create.argtypes = [c_void_p, POINTER(c_void_p)]
        maprclient.hb_admin_create.restype = c_int32

        retCode = maprclient.hb_admin_create(self.connection.connection,
                                             byref(self._admin))
        if retCode != 0:
            raise Exception("Could not create admin: %d".format(retCode))

    def admin_destroy(self, callback=None, extra=None):
        if callback is not None:
            CMPFUNC = CFUNCTYPE(c_int32, hb_admin_disconnection_cb, c_void_p)
            cb = CMPFUNC(callback)
        else:
            cb = None

        maprclient.hb_admin_destroy.argtypes = [c_void_p,
                                                hb_admin_disconnection_cb,
                                                c_void_p]
        maprclient.hb_admin_destroy.restype = c_int32

        retCode = maprclient.hb_admin_destroy(self._admin, cb, )



    def table_exists(self, tableName, nameSpace=None):
        if nameSpace is not None:
            nameSpace = c_char_p(nameSpace)

        tableName = c_char_p(tableName)

        maprclient.hb_admin_table_exists.argtypes = [c_void_p,
                                                     c_char_p,
                                                     c_char_p]
        maprclient.hb_admin_table_exists.restype = c_int32

        retCode = maprclient.hb_admin_table_exists(self._admin,
                                                   nameSpace,
                                                   tableName)
        # TODO: Make this return False if not there, or other if disabled.
        if retCode == 0:
            return True
        else:
            return retCode
