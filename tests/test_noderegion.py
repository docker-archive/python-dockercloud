from __future__ import absolute_import

import unittest

import unittest.mock as mock

import dockercloud
from .fake_api import *


class RegionTestCase(unittest.TestCase):
    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_region_list(self, mock_send):
        attrributes = json.loads(
                '[{"availability_zones": [], "available": true, "label": "Amsterdam 1", "name": "ams1", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/"], "resource_uri": "/api/v1/region/digitalocean/ams1/"}, ' \
                '{"availability_zones": [], "available": true, "label": "San Francisco 1", "name": "sfo1", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/sfo1/"}, ' \
                '{"availability_zones": [], "available": true, "label": "New York 2", "name": "nyc2", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/nyc2/"}, ' \
                '{"availability_zones": [], "available": true, "label": "Amsterdam 2", "name": "ams2", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/ams2/"}, ' \
                '{"availability_zones": [], "available": true, "label": "Singapore 1", "name": "sgp1", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/sgp1/"}, ' \
                '{"availability_zones": [], "available": true, "label": "London 1", "name": "lon1", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/lon1/"}, ' \
                '{"availability_zones": [], "available": true, "label": "New York 3", "name": "nyc3", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/nyc3/"}, ' \
                '{"availability_zones": [], "available": true, "label": "Amsterdam 3", "name": "ams3", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/ams3/"}]'
        )

        mock_send.return_value = fake_resp(fake_region_list)
        regions = dockercloud.Region.list()
        for i in range(0, len(regions)):
            result = json.loads(json.dumps(regions[i].get_all_attributes()))
            target = json.loads(json.dumps(attrributes[i]))
            self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_region_fet(self, mock_send):
        attribute = json.loads(
                '{"availability_zones": [], "available": true, "label": "Amsterdam 1", "name": "ams1", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/"], "provider": "/api/v1/provider/digitalocean/", "resource_uri": "/api/v1/region/digitalocean/ams1/"}'
        )
        mock_send.return_value = fake_resp(fake_region_fetch)
        region = dockercloud.Region.fetch('digitalocean/asm1')
        result = json.loads(json.dumps(region.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)
