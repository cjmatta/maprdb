import unittest
from ..Connection import Connection


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.connection = Connection(autoconnect=False)

    def tearDown(self):
        if self.connection.connected is True:
            self.connection.destroy()

    def test_connected(self):
        self.connection.create()
        self.assertEqual(self.connection.connected, True)

    def test_destroy(self):
        self.connection.create()
        self.connection.destroy()
        self.assertEqual(self.connection.connected, False)

if __name__ == '__main__':
    unittest.main()
