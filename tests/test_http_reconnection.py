import unittest
import time
import dockercloud
from dockercloud.api import http

_reconnection_interval = None

class FakeTime(object):
    def __init__(self, val=None):
        self.val = val
    def time(self):
        return self.val

class SessionReconnectionTestCase(unittest.TestCase):
    # a few helpers
    def setUp(self):
        global _reconnection_interval
        global _last_connection_time
        _reconnection_interval = dockercloud.reconnection_interval
        _last_connection_time = http.last_connection_time
        http.last_connection_time = 0

    def tearDown(self):
        global old_reconnection_interval
        global _last_connection_time
        dockercloud.reconnection_interval = _reconnection_interval
        dockercloud.http = _last_connection_time
    #

    def test_logic_without_interval(self):
        dockercloud.reconnection_interval = None
        session1 = http.get_session()
        session2 = http.get_session()
        self.assertEqual(id(session1), id(session2))

    def test_logic_with_negative_interval(self):
        dockercloud.reconnection_interval = -1
        session1 = http.get_session()
        session2 = http.get_session()
        self.assertEqual(id(session1), id(session2))

    def test_logic_with_zero_interval(self):
        dockercloud.reconnection_interval = 0
        session1 = http.get_session()
        session2 = http.get_session()
        self.assertNotEqual(id(session1), id(session2))

    def test_logic_with_positive_interval(self):
        dockercloud.reconnection_interval = 30

        # diff is less than 30 secs
        session1 = http.get_session(FakeTime(0))
        session2 = http.get_session(FakeTime(10))
        self.assertEqual(id(session1), id(session2))

        # diff is equal to 30 secs
        session3 = http.get_session(FakeTime(40))
        self.assertEqual(id(session2), id(session3))

        # diff is more that 30 secs
        session4 = http.get_session(FakeTime(71))
        self.assertNotEqual(id(session3), id(session4))

