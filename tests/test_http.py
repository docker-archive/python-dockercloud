from __future__ import absolute_import

import unittest

import requests
import unittest.mock as mock

import dockercloud
from dockercloud.api.base import send_request
from .fake_api import fake_resp


class SendRequestTestCase(unittest.TestCase):
    @mock.patch('dockercloud.api.http.Request', return_value=requests.Request('GET', 'http://fake.com'))
    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_http_send_request(self, mock_send, mock_Request):
        json_obj = {'key': 'value'}
        mock_send.return_value = fake_resp(lambda: (None, json_obj))
        self.assertRaises(dockercloud.ApiError, send_request, 'METHOD', 'path', data='data')
        headers = {'Content-Type': 'application/json', 'User-Agent': 'python-dockercloud/%s' % dockercloud.__version__}
        headers.update(dockercloud.auth.get_auth_header())

        mock_send.return_value = fake_resp(lambda: (200, json_obj))
        self.assertEqual(json_obj, send_request('METHOD', 'path'))

        mock_send.return_value = fake_resp(lambda: (204, json_obj))
        self.assertIsNone(send_request('METHOD', 'path'))

        mock_send.return_value = fake_resp(lambda: (401, json_obj))
        self.assertRaises(dockercloud.AuthError, send_request, 'METHOD', 'path')

        mock_send.return_value = fake_resp(lambda: (500, json_obj))
        self.assertRaises(dockercloud.ApiError, send_request, 'METHOD', 'path')
