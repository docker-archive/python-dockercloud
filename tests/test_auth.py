from __future__ import absolute_import

import os
import tempfile
import unittest

import unittest.mock as mock

import dockercloud
from .fake_api import *


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.dockercloud_auth = dockercloud.dockercloud_auth
        self.basic_auth = dockercloud.basic_auth

    def tearDown(self):
        dockercloud.dockercloud_auth = self.dockercloud_auth
        dockercloud.basic_auth = self.basic_auth

    @mock.patch('dockercloud.api.auth.verify_credential')
    def test_auth_authenticate(self, mock_verify_credential):
        dockercloud.auth.authenticate(FAKE_USER, FAKE_PASSWORD)
        mock_verify_credential.assert_called_with(FAKE_USER, FAKE_PASSWORD)
        self.assertEqual(dockercloud.basic_auth, FAKE_BASIC_AUTH)
        self.tearDown()

    def test_auth_is_authenticated(self):
        dockercloud.dockercloud_auth = FAKE_DOCKERCLOUD_AUTH
        dockercloud.basic_auth = FAKE_BASIC_AUTH
        self.assertTrue(dockercloud.auth.is_authenticated())

        dockercloud.dockercloud_auth = None
        dockercloud.basic_auth = FAKE_BASIC_AUTH
        self.assertTrue(dockercloud.auth.is_authenticated())

        dockercloud.dockercloud_auth = FAKE_DOCKERCLOUD_AUTH
        dockercloud.basic_auth = None
        dockercloud.apikey_auth = None
        self.assertTrue(dockercloud.auth.is_authenticated())

        dockercloud.dockercloud_auth = None
        dockercloud.basic_auth = None
        self.assertFalse(dockercloud.auth.is_authenticated())

    def test_auth_logout(self):
        dockercloud.dockercloud_auth = FAKE_DOCKERCLOUD_AUTH
        dockercloud.basic_auth = FAKE_BASIC_AUTH
        dockercloud.auth.logout()
        self.assertIsNone(dockercloud.dockercloud_auth)
        self.assertIsNone(dockercloud.basic_auth)

    def test_auth_load_from_file(self):
        temp = tempfile.NamedTemporaryFile('w', delete=False)
        with temp as f:
            f.write('''{
	"auths": {
		"https://index.docker.io/v1/": {
			"auth": "%s",
			"email": "tifayuki@gmail.com"
		}
	}
}''' % FAKE_BASIC_AUTH)
        basic_auth = dockercloud.auth.load_from_file(f.name)
        self.assertEqual(basic_auth, FAKE_BASIC_AUTH)
        os.remove(temp.name)

    def test_auth_load_from_file_with_exception(self):
        basic_auth = dockercloud.auth.load_from_file('abc')
        self.assertIsNone(basic_auth)

    def test_auth_get_auth_header(self):
        dockercloud.dockercloud_auth = FAKE_DOCKERCLOUD_AUTH
        dockercloud.basic_auth = FAKE_BASIC_AUTH
        self.assertEqual({'Authorization': FAKE_DOCKERCLOUD_AUTH}, dockercloud.auth.get_auth_header())

        print "===================="
        dockercloud.dockercloud_auth = None
        dockercloud.basic_auth = FAKE_BASIC_AUTH
        self.assertEqual({'Authorization': 'Basic %s' % (FAKE_BASIC_AUTH)}, dockercloud.auth.get_auth_header())

        dockercloud.dockercloud_auth = FAKE_DOCKERCLOUD_AUTH
        dockercloud.basic_auth = None
        self.assertEqual({'Authorization': FAKE_DOCKERCLOUD_AUTH}, dockercloud.auth.get_auth_header())

        dockercloud.dockercloud_auth = None
        dockercloud.basic_auth = None
        self.assertEqual({}, dockercloud.auth.get_auth_header())
