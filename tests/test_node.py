from __future__ import absolute_import

import unittest

import unittest.mock as mock

import dockercloud
from .fake_api import *


class NodeTestCase(unittest.TestCase):
    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_node_list(self, mock_send):
        attributes = json.loads(
                '[{"deployed_datetime": "Mon, 29 Sep 2014 22:29:03 +0000", "destroyed_datetime": null, "docker_execdriver": "native-0.2", "docker_graphdriver": "aufs", "docker_version": "1.2.0", "external_fqdn": "fa9df19a-tifayuki.node.docker.io", "last_seen": "Tue, 30 Sep 2014 15:27:05 +0000", "node_cluster": "/api/v1/nodecluster/a02c3763-e639-46fc-a6db-587f4dbb5444/", "node_type": "/api/v1/nodetype/digitalocean/512mb/", "public_ip": "198.199.97.190", "region": "/api/v1/region/digitalocean/sfo1/", "resource_uri": "/api/v1/node/fa9df19a-162b-45b4-bb5a-152dfd1b133f/", "state": "Deployed", "uuid": "fa9df19a-162b-45b4-bb5a-152dfd1b133f"}, ' \
                '{"deployed_datetime": "Mon, 29 Sep 2014 22:59:47 +0000", "destroyed_datetime": null, "docker_execdriver": "native-0.2", "docker_graphdriver": "aufs", "docker_version": "1.2.0", "external_fqdn": "43b5ebaf-tifayuki.node.docker.io", "last_seen": "Tue, 30 Sep 2014 15:27:06 +0000", "node_cluster": "/api/v1/nodecluster/b616a720-6684-42c6-83bb-4d298b11b3f3/", "node_type": "/api/v1/nodetype/digitalocean/512mb/", "public_ip": "178.62.20.100", "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/node/43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456/", "state": "Deployed", "uuid": "43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456"}]'
        )
        mock_send.return_value = fake_resp(fake_node_list)
        nodes = dockercloud.Node.list()
        for i in range(0, len(nodes)):
            result = json.loads(json.dumps(nodes[i].get_all_attributes()))
            target = json.loads(json.dumps(attributes[i]))
            self.assertDictEqual(target, result)

    def test_node_save(self):
        self.assertRaises(AttributeError, dockercloud.Node().save)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_node_fetch(self, mock_send):
        attribute = json.loads(
                '{"actions": ["/api/v1/action/8f5b893b-826e-40b7-bb8b-2d96301425f2/"], "deployed_datetime": "Mon, 29 Sep 2014 22:59:47 +0000", "destroyed_datetime": null, "docker_execdriver": "native-0.2", "docker_graphdriver": "aufs", "docker_version": "1.2.0", "external_fqdn": "43b5ebaf-tifayuki.node.docker.io", "last_seen": "Tue, 30 Sep 2014 15:30:06 +0000", "node_cluster": "/api/v1/nodecluster/b616a720-6684-42c6-83bb-4d298b11b3f3/", "node_type": "/api/v1/nodetype/digitalocean/512mb/", "public_ip": "178.62.20.100", "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/node/43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456/", "state": "Deployed", "uuid": "43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456"}'
        )
        mock_send.return_value = fake_resp(fake_node_fetch)
        node = dockercloud.Node.fetch('43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456')
        result = json.loads(json.dumps(node.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_node_delete(self, mock_send):
        attribute = json.loads(
                '{"actions": ["/api/v1/action/8f5b893b-826e-40b7-bb8b-2d96301425f2/", "/api/v1/action/83c66611-ea5d-45d7-a97d-914029a90524/"], "deployed_datetime": "Mon, 29 Sep 2014 22:59:47 +0000", "destroyed_datetime": null, "docker_execdriver": "native-0.2", "docker_graphdriver": "aufs", "docker_version": "1.2.0", "external_fqdn": "43b5ebaf-tifayuki.node.docker.io", "last_seen": "Tue, 30 Sep 2014 15:38:12 +0000", "node_cluster": "/api/v1/nodecluster/b616a720-6684-42c6-83bb-4d298b11b3f3/", "node_type": "/api/v1/nodetype/digitalocean/512mb/", "public_ip": "178.62.20.100", "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/node/43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456/", "state": "Terminating", "uuid": "43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456"}'
        )
        mock_send.return_value = fake_resp(fake_node_delete)
        node = dockercloud.Node.fetch('43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456')
        self.assertTrue(node.delete())
        result = json.loads(json.dumps(node.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_node_deploy(self, mock_send):
        attribute = json.loads(
                '{"actions": ["/api/v1/action/8f5b893b-826e-40b7-bb8b-2d96301425f2/", "/api/v1/action/83c66611-ea5d-45d7-a97d-914029a90524/"], "deployed_datetime": "Mon, 29 Sep 2014 22:59:47 +0000", "destroyed_datetime": null, "docker_execdriver": "native-0.2", "docker_graphdriver": "aufs", "docker_version": "1.2.0", "external_fqdn": "43b5ebaf-tifayuki.node.docker.io", "last_seen": "Tue, 30 Sep 2014 15:38:12 +0000", "node_cluster": "/api/v1/nodecluster/b616a720-6684-42c6-83bb-4d298b11b3f3/", "node_type": "/api/v1/nodetype/digitalocean/512mb/", "public_ip": "178.62.20.100", "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/node/43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456/", "state": "Starting", "uuid": "43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456"}'
        )
        mock_send.return_value = fake_resp(fake_node_deploy)
        node = dockercloud.Node.fetch('43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456')
        self.assertTrue(node.deploy())
        result = json.loads(json.dumps(node.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)
