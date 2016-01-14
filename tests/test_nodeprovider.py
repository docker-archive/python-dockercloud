from __future__ import absolute_import

import unittest

import unittest.mock as mock

import dockercloud
from .fake_api import *


class ProviderTestCase(unittest.TestCase):
    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_provider_list(self, mock_send):
        attributes = json.loads(
                '[{"available": true, "label": "Digital Ocean", "name": "digitalocean", "regions": ["/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/ams3/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/sgp1/"], "resource_uri": "/api/v1/provider/digitalocean/"}]'
        )
        mock_send.return_value = fake_resp(fake_provider_list)
        providers = dockercloud.Provider.list()
        for i in range(0, len(providers)):
            result = json.loads(json.dumps(providers[i].get_all_attributes()))
            target = json.loads(json.dumps(attributes[i]))
            self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_provider_fetch(self, mock_send):
        attribute = json.loads(
                '{"available": true, "label": "Digital Ocean", "name": "digitalocean", "regions": ["/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/ams3/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/sgp1/"], "resource_uri": "/api/v1/provider/digitalocean/"}'
        )
        mock_send.return_value = fake_resp(fake_provider_fetch)
        provider = dockercloud.Provider.fetch("digitalocean")
        result = json.loads(json.dumps(provider.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)
