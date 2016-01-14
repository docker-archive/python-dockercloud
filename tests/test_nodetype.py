from __future__ import absolute_import

import unittest

import unittest.mock as mock

import dockercloud
from .fake_api import *


class NodeTypeTestCase(unittest.TestCase):
    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_nodetype_list(self, mock_send):
        attributes = json.loads(
                '[{"availability_zones": [], "available": true, "label": "512MB", "name": "512mb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/512mb/"}, ' \
                '{"availability_zones": [], "available": true, "label": "1GB", "name": "1gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/1gb/"}, ' \
                '{"availability_zones": [], "available": true, "label": "2GB", "name": "2gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/2gb/"}, ' \
                '{"availability_zones": [], "available": true, "label": "4GB", "name": "4gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/4gb/"}, ' \
                '{"availability_zones": [], "available": true, "label": "8GB", "name": "8gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/8gb/"}, ' \
                '{"availability_zones": [], "available": true, "label": "16GB", "name": "16gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/16gb/"}, ' \
                '{"availability_zones": [], "available": true, "label": "32GB", "name": "32gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/32gb/"}, ' \
                '{"availability_zones": [], "available": true, "label": "48GB", "name": "48gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/48gb/"}, ' \
                '{"availability_zones": [], "available": true, "label": "64GB", "name": "64gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/64gb/"}]'
        )
        mock_send.return_value = fake_resp(fake_nodetype_list)
        nodetypes = dockercloud.NodeType.list()
        for i in range(0, len(nodetypes)):
            result = json.loads(json.dumps(nodetypes[i].get_all_attributes()))
            target = json.loads(json.dumps(attributes[i]))
            self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_nodetype_fetch(self, mock_send):
        attribute = json.loads(
                '{"availability_zones": [], "available": true, "label": "8GB", "name": "8gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/8gb/"}'
        )
        mock_send.return_value = fake_resp(fake_nodetype_fetch)
        nodetype = dockercloud.NodeType.fetch('digitalocean/8gb')
        result = json.loads(json.dumps(nodetype.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)
