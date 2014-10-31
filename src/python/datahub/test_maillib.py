from maillib import Gmail, GmailParser
from nose.tools import *
import unittest
import simplejson as json


class TestGmail(unittest.TestCase):

    def setUp(self):
        f = open("test_mailaccount.json")
        data = json.load(f)
        self.account = Gmail(data)

    def tearDown(self):
        self.account = None

    def test_connect(self):
        self.account.connect()
        assert self.account.server is not None

    def test_folders(self):
        self.account.connect()
        actual = self.account.get_folders()
        assert actual is not []
        assert len(actual) > 0
    @raises(Exception)
    def test_incorrect_account(self):
        self.account.pwd = "NOWAYJOSE"
        self.account.connect()
        print self.account.server
        assert self.account.server is None
