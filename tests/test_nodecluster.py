from __future__ import absolute_import

import unittest

import unittest.mock as mock

import dockercloud
from .fake_api import *


class NodeClusterTestCase(unittest.TestCase):
    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_nodecluster_list(self, mock_send):
        attributes = json.loads(
                '[{"current_num_nodes": 1, "deployed_datetime": "Mon, 29 Sep 2014 22:29:03 +0000", "destroyed_datetime": null, "name": "test", "node_type": "/api/v1/nodetype/digitalocean/512mb/", "region": "/api/v1/region/digitalocean/sfo1/", "resource_uri": "/api/v1/nodecluster/a02c3763-e639-46fc-a6db-587f4dbb5444/", "state": "Deployed", "target_num_nodes": 1, "uuid": "a02c3763-e639-46fc-a6db-587f4dbb5444"}, '
                '{"current_num_nodes": 1, "deployed_datetime": null, "destroyed_datetime": null, "name": "test2", "node_type": "/api/v1/nodetype/digitalocean/512mb/", "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/nodecluster/b616a720-6684-42c6-83bb-4d298b11b3f3/", "state": "Deploying", "target_num_nodes": 1, "uuid": "b616a720-6684-42c6-83bb-4d298b11b3f3"}]'
        )
        mock_send.return_value = fake_resp(fake_nodeclster_list)
        clusters = dockercloud.NodeCluster.list()
        for i in range(0, len(clusters)):
            result = json.loads(json.dumps(clusters[i].get_all_attributes()))
            target = json.loads(json.dumps(attributes[i]))
            self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_nodecluster_fetch(self, mock_send):
        attribute = json.loads(
                '{"actions": ["/api/v1/action/bf02b00a-e2fc-4098-8b69-1424b659ef4a/", "/api/v1/action/f8dce6d4-5c41-46a9-9754-baa8f3cdf031/"], "current_num_nodes": 1, "deployed_datetime": null, "destroyed_datetime": null, "name": "test2", "node_type": "/api/v1/nodetype/digitalocean/512mb/", "nodes": ["/api/v1/node/43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456/"], "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/nodecluster/b616a720-6684-42c6-83bb-4d298b11b3f3/", "state": "Init", "target_num_nodes": 1, "uuid": "b616a720-6684-42c6-83bb-4d298b11b3f3"}'
        )
        mock_send.return_value = fake_resp(fake_nodecluster_fetch)
        cluster = dockercloud.NodeCluster.fetch('b616a720-6684-42c6-83bb-4d298b11b3f3')
        result = json.loads(json.dumps(cluster.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_nodecluster_save(self, mock_send):
        attribute = json.loads(
                '{"actions": ["/api/v1/action/f47e26a6-c60c-416f-a0a9-ddf14e3aae83/"], "current_num_nodes": 1, "deployed_datetime": null, "destroyed_datetime": null, "name": "my_cluster", "node_type": "/api/v1/nodetype/digitalocean/1gb/", "nodes": ["/api/v1/node/2cfe7823-f551-4c7b-a82c-f6ab31d7ca25/"], "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/nodecluster/e7915a74-618b-4908-9189-dce965465702/", "state": "Init", "target_num_nodes": 1, "uuid": "e7915a74-618b-4908-9189-dce965465702"}'
        )
        mock_send.return_value = fake_resp(fake_nodecluster_save)
        cluster = dockercloud.NodeCluster.create(name="my_cluster", region="/api/v1/region/digitalocean/lon1/",
                                                 node_type="/api/v1/nodetype/digitalocean/1gb/")
        self.assertTrue(cluster.save())
        result = json.loads(json.dumps(cluster.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_nodecluster_deploy(self, mock_send):
        attribute = json.loads(
                '{"actions": ["/api/v1/action/f47e26a6-c60c-416f-a0a9-ddf14e3aae83/", "/api/v1/action/d110016e-e65d-4ce7-9f11-50c6302494a6/"], "current_num_nodes": 1, "deployed_datetime": null, "destroyed_datetime": null, "name": "my_cluster", "node_type": "/api/v1/nodetype/digitalocean/1gb/", "nodes": ["/api/v1/node/2cfe7823-f551-4c7b-a82c-f6ab31d7ca25/"], "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/nodecluster/e7915a74-618b-4908-9189-dce965465702/", "state": "Deploying", "target_num_nodes": 1, "uuid": "e7915a74-618b-4908-9189-dce965465702"}'
        )
        mock_send.side_effect = [fake_resp(fake_nodecluster_save), fake_resp(fake_nodecluster_deploy)]
        cluster = dockercloud.NodeCluster.create(name="my_cluster", region="/api/v1/region/digitalocean/lon1/",
                                                 node_type="/api/v1/nodetype/digitalocean/1gb/")
        cluster.save()
        self.assertTrue(cluster.deploy())
        result = json.loads(json.dumps(cluster.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_nodecluster_delete(self, mock_send):
        attribute = json.loads(
                '{"actions": ["/api/v1/action/f47e26a6-c60c-416f-a0a9-ddf14e3aae83/", "/api/v1/action/d110016e-e65d-4ce7-9f11-50c6302494a6/", "/api/v1/action/e33b4bb1-192b-46a6-a1ba-eadfc494c2dd/"], "current_num_nodes": 1, "deployed_datetime": "Mon, 29 Sep 2014 23:45:45 +0000", "destroyed_datetime": null, "name": "my_cluster", "node_type": "/api/v1/nodetype/digitalocean/1gb/", "nodes": ["/api/v1/node/2cfe7823-f551-4c7b-a82c-f6ab31d7ca25/"], "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/nodecluster/e7915a74-618b-4908-9189-dce965465702/", "state": "Terminating", "target_num_nodes": 0, "uuid": "e7915a74-618b-4908-9189-dce965465702"}'
        )
        mock_send.return_value = fake_resp(fake_nodecluster_delete)
        cluster = dockercloud.NodeCluster.fetch('e7915a74-618b-4908-9189-dce965465702')
        self.assertTrue(cluster.delete())
        result = json.loads(json.dumps(cluster.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)
