from ctypes import *

try:
    maprclient = CDLL("/opt/mapr/lib/libMapRClient.dylib.1")
except Exception, e:
    raise e


class Connection(object):
    def __init__(self,
                 zkQuorum=None,
                 zkRootNode=None,
                 autoconnect=True):
        self.zkQuorum = zkQuorum
        self.zkRootNode = zkRootNode
        self._zkQuorum = c_char_p(self.zkQuorum)
        self._zkRootNode = c_char_p(self.zkRootNode)
        self.connection = c_void_p()
        self.connected = False
        self.autoconnect = autoconnect

        if self.autoconnect is True:
            self.create()

    def create(self):
        if self.connection.value is None:
            # declare argtypes for hb_connection_create
            maprclient.hb_connection_create.argtypes = [c_char_p, c_char_p,
                                                        POINTER(c_void_p)]
            # declare return type for hb_connection_create
            maprclient.hb_connection_create.restype = c_int32
            retCode = maprclient.hb_connection_create(self._zkQuorum,
                                                      self._zkRootNode,
                                                      byref(self.connection))
            if(retCode != 0):
                raise Exception("Could not connect to {0}: {1}".format(
                                    self.zkQuorum, retCode)
                                )
            else:
                self.connected = True

    def destroy(self):
        if self.connection.value is not None:
            maprclient.hb_connection_destroy.argtypes = [c_void_p]
            maprclient.hb_connection_destroy.restype = c_int32

            retCode = maprclient.hb_connection_destroy(self.connection)

            if (retCode != 0):
                raise Exception("Could not destroy connection.")
            else:
                self.connected = False
