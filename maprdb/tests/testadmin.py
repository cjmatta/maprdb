import unittest
from ..Admin import Admin


class TestAdmin(unittest.TestCase):
    def setUp(self):
        self.admin = Admin()

    def tearDown(self):
        self.admin.destroy()

    def test_admin_created(self):
        self.assertIsNot(self.admin._admin, None)

    def test_admin_destroyed(self):
        self.assertIs(self.admin._admin, None)
