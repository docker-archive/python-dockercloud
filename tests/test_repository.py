from __future__ import absolute_import

import unittest

import unittest.mock as mock

import dockercloud
from .fake_api import *


class ImageTestCase(unittest.TestCase):
    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_image_list(self, mock_send):
        attributes = json.loads(
                '[{"base_image": false, "categories": [], "cluster_aware": true, "description": "", "docker_registry": "/api/v1/registry/docker.com/", "image_url": "", "imagetag_set": ["/api/v1/image/docker.com/tifayuki/mongodb/tag/latest/"], "is_private_image": true, "name": "docker.com/tifayuki/mongodb", "public_url": "", "resource_uri": "/api/v1/image/docker.com/tifayuki/mongodb/", "starred": false}]'
        )
        mock_send.return_value = fake_resp(fake_image_list)
        images = dockercloud.Repository.list()
        for i in range(0, len(images)):
            result = json.loads(json.dumps(images[i].get_all_attributes()))
            target = json.loads(json.dumps(attributes[i]))
            self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_image_fetch(self, mock_send):
        attribute = json.loads(
                '{"base_image": false, "categories": [], "cluster_aware": true, "description": "", "docker_registry": {"created": true, "host": "registry.hub.docker.com", "id": 5, "image_url": "/_static/assets/images/dockerregistries/docker.png", "is_ssl": true, "is_tutum_registry": false, "modified": true, "name": "Docker.io", "resource_uri": "/api/v1/registry/registry.hub.docker.com/", "uuid": "d533039e-c44c-4cdc-951b-e0e03b8410c6"}, "image_url": "", "imagetag_set": [{"full_name": "tifayuki/cadvisor:latest", "image": {"author": "fake <fake@docker.com>", "docker_id": "9e2907ef52bf811b4da100f50ba8f0908ccc610c7054bd69087f0a9f4703efdd", "entrypoint": "", "image_creation": "Fri, 15 Aug 2014 15:19:04 +0000", "imageenvvar_set": [{"key": "CADVISOR_TAG", "value": "0.2.2"}, {"key": "DB_NAME", "value": "cadvisor"}, {"key": "DB_PASS", "value": "root"}, {"key": "DB_USER", "value": "root"}, {"key": "HOME", "value": "/"}, {"key": "PATH", "value": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"}], "imageport_set": [], "run_command": "/run.sh"}, "image_info": "/api/v1/image/tifayuki/cadvisor/", "name": "latest", "resource_uri": "/api/v1/image/tifayuki/cadvisor/tag/latest/"}], "is_private_image": true, "name": "tifayuki/cadvisor", "public_url": "https://registry.hub.docker.com/u/tifayuki/cadvisor/", "resource_uri": "/api/v1/image/tifayuki/cadvisor/", "starred": false}'
        )
        mock_send.return_value = fake_resp(fake_image_fetch)
        image = dockercloud.Repository.fetch('tifayuki/cadvisor')
        result = json.loads(json.dumps(image.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_image_save(self, mock_send):
        attribute = json.loads(
                '{"base_image": false, "categories": [], "cluster_aware": true, "description": "description", "docker_registry": {"created": true, "host": "registry.hub.docker.com", "id": 5, "image_url": "/_static/assets/images/dockerregistries/docker.png", "is_ssl": true, "is_tutum_registry": false, "modified": true, "name": "Docker.io", "resource_uri": "/api/v1/registry/registry.hub.docker.com/", "uuid": "d533039e-c44c-4cdc-951b-e0e03b8410c6"}, "image_url": "", "imagetag_set": [{"full_name": "tifayuki/cadvisor:latest", "image": {"author": "fake <fake@docker.com>", "docker_id": "9e2907ef52bf811b4da100f50ba8f0908ccc610c7054bd69087f0a9f4703efdd", "entrypoint": "", "image_creation": "Fri, 15 Aug 2014 15:19:04 +0000", "imageenvvar_set": [{"key": "CADVISOR_TAG", "value": "0.2.2"}, {"key": "DB_NAME", "value": "cadvisor"}, {"key": "DB_PASS", "value": "root"}, {"key": "DB_USER", "value": "root"}, {"key": "HOME", "value": "/"}, {"key": "PATH", "value": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"}], "imageport_set": [], "run_command": "/run.sh"}, "image_info": "/api/v1/image/tifayuki/cadvisor/", "name": "latest", "resource_uri": "/api/v1/image/tifayuki/cadvisor/tag/latest/"}], "is_private_image": true, "name": "tifayuki/cadvisor", "public_url": "https://registry.hub.docker.com/u/tifayuki/cadvisor/", "resource_uri": "/api/v1/image/tifayuki/cadvisor/", "starred": false}'
        )
        mock_send.return_value = fake_resp(fake_image_save)
        image = dockercloud.Repository.fetch('tifayuki/cadvisor')
        image.description = 'descripiton'
        self.assertTrue(image.save())
        result = json.loads(json.dumps(image.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_image_delete(self, mock_send):
        mock_send.side_effect = [fake_resp(fake_image_fetch), fake_resp(fake_image_delete)]
        image = dockercloud.Repository.fetch('tifayuki/cadvisor')
        self.assertTrue(image.delete())
