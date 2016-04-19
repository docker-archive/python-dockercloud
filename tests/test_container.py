from __future__ import absolute_import

import unittest

import unittest.mock as mock

import dockercloud
from .fake_api import *


class ContainerTestCase(unittest.TestCase):
    def setUp(self):
        dockercloud.api.http.invalid_auth_headers = []

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_container_list(self, mock_send):
        attributes = json.loads(
            '[{"autodestroy": "OFF", "autoreplace": "OFF", "autorestart": "OFF", "container_ports": [{"endpoint_uri": "mysql://mysql-1.fa9df19a-tifayuki.node.docker.io:49159/", "inner_port": 3306, "outer_port": 49159, "port_name": "mysql", "protocol": "tcp", "uri_protocol": "mysql"}], "cpu_shares": null, "deployed_datetime": "Wed, 1 Oct 2014 14:44:32 +0000", "destroyed_datetime": null, "entrypoint": "", "exit_code": null, "exit_code_msg": null, "image_name": "tutum/mysql:latest", "image_tag": "/api/v1/image/tutum/mysql/tag/latest/", "is_dead_backend": null, "memory": null, "memory_swap": null, "name": "mysql", "node": "/api/v1/node/fa9df19a-162b-45b4-bb5a-152dfd1b133f/", "public_dns": "mysql-1.fa9df19a-tifayuki.node.docker.io", "resource_uri": "/api/v1/container/567f1ff8-57bd-4689-a732-1e1705bc5082/", "run_command": "/run.sh", "service": "/api/v1/service/326a2daf-2069-4cd4-9e44-08faa068a62f/", "started_datetime": "Wed, 1 Oct 2014 14:44:32 +0000", "state": "Running", "stopped_datetime": null, "unique_name": "mysql-1", "uuid": "567f1ff8-57bd-4689-a732-1e1705bc5082"}, {"autodestroy": "OFF", "autoreplace": "OFF", "autorestart": "OFF", "container_ports": [{"endpoint_uri": "http://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160/", "inner_port": 80, "outer_port": 49160, "port_name": "http", "protocol": "tcp", "uri_protocol": "http"}, {"endpoint_uri": "mysql://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161/", "inner_port": 3306, "outer_port": 49161, "port_name": "mysql", "protocol": "tcp", "uri_protocol": "mysql"}], "cpu_shares": null, "deployed_datetime": "Wed, 1 Oct 2014 14:54:23 +0000", "destroyed_datetime": null, "entrypoint": "", "exit_code": null, "exit_code_msg": null, "image_name": "tutum/wordpress:latest", "image_tag": "/api/v1/image/tutum/wordpress/tag/latest/", "is_dead_backend": null, "memory": null, "memory_swap": null, "name": "wordpress", "node": "/api/v1/node/fa9df19a-162b-45b4-bb5a-152dfd1b133f/", "public_dns": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "resource_uri": "/api/v1/container/52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d/", "run_command": "/run.sh", "service": "/api/v1/service/81bbc30a-35de-4f5e-840d-87bc2573d818/", "started_datetime": "Wed, 1 Oct 2014 14:54:23 +0000", "state": "Running", "stopped_datetime": null, "unique_name": "wordpress-1", "uuid": "52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d"}]'
        )
        mock_send.return_value = fake_resp(fake_container_list)
        containers = dockercloud.Container.list()
        for i in range(0, len(containers)):
            result = json.loads(json.dumps(containers[i].get_all_attributes()))
            target = json.loads(json.dumps(attributes[i]))
            self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_container_fetch(self, mock_send):
        attribute = json.loads(
            '{"actions": ["/api/v1/action/62b1f681-5c0a-4b4e-8bc7-570f62020711/"], "autodestroy": "OFF", "autoreplace": "OFF", "autorestart": "OFF", "container_envvars": [], "container_ports": [{"endpoint_uri": "http://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160/", "inner_port": 80, "outer_port": 49160, "port_name": "http", "protocol": "tcp", "uri_protocol": "http"}, {"endpoint_uri": "mysql://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161/", "inner_port": 3306, "outer_port": 49161, "port_name": "mysql", "protocol": "tcp", "uri_protocol": "mysql"}], "cpu_shares": null, "deployed_datetime": "Wed, 1 Oct 2014 14:54:23 +0000", "destroyed_datetime": null, "entrypoint": "", "exit_code": null, "exit_code_msg": null, "image_name": "tutum/wordpress:latest", "image_tag": "/api/v1/image/tutum/wordpress/tag/latest/", "is_dead_backend": null, "link_variables": {"WORDPRESS_1_ENV_HOME": "/", "WORDPRESS_1_ENV_PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "WORDPRESS_1_ENV_PHP_POST_MAX_SIZE": "10M", "WORDPRESS_1_ENV_PHP_UPLOAD_MAX_FILESIZE": "10M", "WORDPRESS_1_PORT_3306_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161", "WORDPRESS_1_PORT_3306_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_1_PORT_3306_TCP_PORT": "49161", "WORDPRESS_1_PORT_3306_TCP_PROTO": "tcp", "WORDPRESS_1_PORT_80_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160", "WORDPRESS_1_PORT_80_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_1_PORT_80_TCP_PORT": "49160", "WORDPRESS_1_PORT_80_TCP_PROTO": "tcp", "WORDPRESS_ENV_HOME": "/", "WORDPRESS_ENV_PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "WORDPRESS_ENV_PHP_POST_MAX_SIZE": "10M", "WORDPRESS_ENV_PHP_UPLOAD_MAX_FILESIZE": "10M", "WORDPRESS_PORT_3306_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161", "WORDPRESS_PORT_3306_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_PORT_3306_TCP_PORT": "49161", "WORDPRESS_PORT_3306_TCP_PROTO": "tcp", "WORDPRESS_PORT_80_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160", "WORDPRESS_PORT_80_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_PORT_80_TCP_PORT": "49160", "WORDPRESS_PORT_80_TCP_PROTO": "tcp"}, "memory": null, "memory_swap": null, "name": "wordpress", "node": "/api/v1/node/fa9df19a-162b-45b4-bb5a-152dfd1b133f/", "public_dns": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "resource_uri": "/api/v1/container/52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d/", "roles": [], "run_command": "/run.sh", "service": "/api/v1/service/81bbc30a-35de-4f5e-840d-87bc2573d818/", "started_datetime": "Wed, 1 Oct 2014 14:54:23 +0000", "state": "Running", "stopped_datetime": null, "unique_name": "wordpress-1", "uuid": "52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d"}'
        )
        mock_send.return_value = fake_resp(fake_container_fetch)
        container = dockercloud.Container.fetch('52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d')
        self.assertTrue(container.start())
        result = json.loads(json.dumps(container.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_container_delete(self, mock_send):
        attribute = json.loads(
            '{"actions": ["/api/v1/action/62b1f681-5c0a-4b4e-8bc7-570f62020711/", "/api/v1/action/5c435933-a1d9-449e-acb6-fbe7b5904b26/", "/api/v1/action/2508d37c-57a8-4ef1-88ff-3b5e20f88b7f/", "/api/v1/action/0438248f-b05c-41f2-b715-40a788735deb/", "/api/v1/action/6a5b82a0-b14a-4c05-94d0-117d730cb647/"], "autodestroy": "OFF", "autoreplace": "OFF", "autorestart": "OFF", "container_envvars": [], "container_ports": [{"endpoint_uri": "http://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160/", "inner_port": 80, "outer_port": 49160, "port_name": "http", "protocol": "tcp", "uri_protocol": "http"}, {"endpoint_uri": "mysql://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161/", "inner_port": 3306, "outer_port": 49161, "port_name": "mysql", "protocol": "tcp", "uri_protocol": "mysql"}], "cpu_shares": null, "deployed_datetime": "Wed, 1 Oct 2014 14:54:23 +0000", "destroyed_datetime": null, "entrypoint": "", "exit_code": 0, "exit_code_msg": "Exit code 0 (Success)", "image_name": "tutum/wordpress:latest", "image_tag": "/api/v1/image/tutum/wordpress/tag/latest/", "is_dead_backend": null, "link_variables": {"WORDPRESS_1_ENV_HOME": "/", "WORDPRESS_1_ENV_PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "WORDPRESS_1_ENV_PHP_POST_MAX_SIZE": "10M", "WORDPRESS_1_ENV_PHP_UPLOAD_MAX_FILESIZE": "10M", "WORDPRESS_1_PORT_3306_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161", "WORDPRESS_1_PORT_3306_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_1_PORT_3306_TCP_PORT": "49161", "WORDPRESS_1_PORT_3306_TCP_PROTO": "tcp", "WORDPRESS_1_PORT_80_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160", "WORDPRESS_1_PORT_80_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_1_PORT_80_TCP_PORT": "49160", "WORDPRESS_1_PORT_80_TCP_PROTO": "tcp", "WORDPRESS_ENV_HOME": "/", "WORDPRESS_ENV_PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "WORDPRESS_ENV_PHP_POST_MAX_SIZE": "10M", "WORDPRESS_ENV_PHP_UPLOAD_MAX_FILESIZE": "10M", "WORDPRESS_PORT_3306_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161", "WORDPRESS_PORT_3306_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_PORT_3306_TCP_PORT": "49161", "WORDPRESS_PORT_3306_TCP_PROTO": "tcp", "WORDPRESS_PORT_80_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160", "WORDPRESS_PORT_80_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_PORT_80_TCP_PORT": "49160", "WORDPRESS_PORT_80_TCP_PROTO": "tcp"}, "memory": null, "memory_swap": null, "name": "wordpress", "node": "/api/v1/node/fa9df19a-162b-45b4-bb5a-152dfd1b133f/", "public_dns": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "resource_uri": "/api/v1/container/52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d/", "roles": [], "run_command": "/run.sh", "service": "/api/v1/service/81bbc30a-35de-4f5e-840d-87bc2573d818/", "started_datetime": "Wed, 1 Oct 2014 15:22:51 +0000", "state": "Terminating", "stopped_datetime": "Wed, 1 Oct 2014 15:20:58 +0000", "unique_name": "wordpress-1", "uuid": "52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d"}'
        )
        mock_send.side_effect = [fake_resp(fake_container_fetch), fake_resp(fake_container_delete)]
        container = dockercloud.Container.fetch('52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d')
        self.assertTrue(container.delete())
        result = json.loads(json.dumps(container.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_container_start(self, mock_send):
        attribute = json.loads(
            '{"actions": ["/api/v1/action/62b1f681-5c0a-4b4e-8bc7-570f62020711/", "/api/v1/action/5c435933-a1d9-449e-acb6-fbe7b5904b26/", "/api/v1/action/2508d37c-57a8-4ef1-88ff-3b5e20f88b7f/"], "autodestroy": "OFF", "autoreplace": "OFF", "autorestart": "OFF", "container_envvars": [], "container_ports": [{"endpoint_uri": "http://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160/", "inner_port": 80, "outer_port": 49160, "port_name": "http", "protocol": "tcp", "uri_protocol": "http"}, {"endpoint_uri": "mysql://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161/", "inner_port": 3306, "outer_port": 49161, "port_name": "mysql", "protocol": "tcp", "uri_protocol": "mysql"}], "cpu_shares": null, "deployed_datetime": "Wed, 1 Oct 2014 14:54:23 +0000", "destroyed_datetime": null, "entrypoint": "", "exit_code": 0, "exit_code_msg": "Exit code 0 (Success)", "image_name": "tutum/wordpress:latest", "image_tag": "/api/v1/image/tutum/wordpress/tag/latest/", "is_dead_backend": null, "link_variables": {"WORDPRESS_1_ENV_HOME": "/", "WORDPRESS_1_ENV_PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "WORDPRESS_1_ENV_PHP_POST_MAX_SIZE": "10M", "WORDPRESS_1_ENV_PHP_UPLOAD_MAX_FILESIZE": "10M", "WORDPRESS_1_PORT_3306_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161", "WORDPRESS_1_PORT_3306_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_1_PORT_3306_TCP_PORT": "49161", "WORDPRESS_1_PORT_3306_TCP_PROTO": "tcp", "WORDPRESS_1_PORT_80_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160", "WORDPRESS_1_PORT_80_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_1_PORT_80_TCP_PORT": "49160", "WORDPRESS_1_PORT_80_TCP_PROTO": "tcp", "WORDPRESS_ENV_HOME": "/", "WORDPRESS_ENV_PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "WORDPRESS_ENV_PHP_POST_MAX_SIZE": "10M", "WORDPRESS_ENV_PHP_UPLOAD_MAX_FILESIZE": "10M", "WORDPRESS_PORT_3306_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161", "WORDPRESS_PORT_3306_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_PORT_3306_TCP_PORT": "49161", "WORDPRESS_PORT_3306_TCP_PROTO": "tcp", "WORDPRESS_PORT_80_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160", "WORDPRESS_PORT_80_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_PORT_80_TCP_PORT": "49160", "WORDPRESS_PORT_80_TCP_PROTO": "tcp"}, "memory": null, "memory_swap": null, "name": "wordpress", "node": "/api/v1/node/fa9df19a-162b-45b4-bb5a-152dfd1b133f/", "public_dns": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "resource_uri": "/api/v1/container/52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d/", "roles": [], "run_command": "/run.sh", "service": "/api/v1/service/81bbc30a-35de-4f5e-840d-87bc2573d818/", "started_datetime": "Wed, 1 Oct 2014 14:54:23 +0000", "state": "Starting", "stopped_datetime": "Wed, 1 Oct 2014 15:20:58 +0000", "unique_name": "wordpress-1", "uuid": "52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d"}'
        )
        mock_send.side_effect = [fake_resp(fake_container_fetch), fake_resp(fake_container_start)]
        container = dockercloud.Container.fetch('52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d')
        self.assertTrue(container.start())
        result = json.loads(json.dumps(container.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_container_stop(self, mock_send):
        attribute = json.loads(
            '{"actions": ["/api/v1/action/62b1f681-5c0a-4b4e-8bc7-570f62020711/"], "autodestroy": "OFF", "autoreplace": "OFF", "autorestart": "OFF", "container_envvars": [], "container_ports": [{"endpoint_uri": "http://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160/", "inner_port": 80, "outer_port": 49160, "port_name": "http", "protocol": "tcp", "uri_protocol": "http"}, {"endpoint_uri": "mysql://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161/", "inner_port": 3306, "outer_port": 49161, "port_name": "mysql", "protocol": "tcp", "uri_protocol": "mysql"}], "cpu_shares": null, "deployed_datetime": "Wed, 1 Oct 2014 14:54:23 +0000", "destroyed_datetime": null, "entrypoint": "", "exit_code": null, "exit_code_msg": null, "image_name": "tutum/wordpress:latest", "image_tag": "/api/v1/image/tutum/wordpress/tag/latest/", "is_dead_backend": null, "link_variables": {"WORDPRESS_1_ENV_HOME": "/", "WORDPRESS_1_ENV_PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "WORDPRESS_1_ENV_PHP_POST_MAX_SIZE": "10M", "WORDPRESS_1_ENV_PHP_UPLOAD_MAX_FILESIZE": "10M", "WORDPRESS_1_PORT_3306_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161", "WORDPRESS_1_PORT_3306_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_1_PORT_3306_TCP_PORT": "49161", "WORDPRESS_1_PORT_3306_TCP_PROTO": "tcp", "WORDPRESS_1_PORT_80_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160", "WORDPRESS_1_PORT_80_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_1_PORT_80_TCP_PORT": "49160", "WORDPRESS_1_PORT_80_TCP_PROTO": "tcp", "WORDPRESS_ENV_HOME": "/", "WORDPRESS_ENV_PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "WORDPRESS_ENV_PHP_POST_MAX_SIZE": "10M", "WORDPRESS_ENV_PHP_UPLOAD_MAX_FILESIZE": "10M", "WORDPRESS_PORT_3306_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49161", "WORDPRESS_PORT_3306_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_PORT_3306_TCP_PORT": "49161", "WORDPRESS_PORT_3306_TCP_PROTO": "tcp", "WORDPRESS_PORT_80_TCP": "tcp://wordpress-1.fa9df19a-tifayuki.node.docker.io:49160", "WORDPRESS_PORT_80_TCP_ADDR": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "WORDPRESS_PORT_80_TCP_PORT": "49160", "WORDPRESS_PORT_80_TCP_PROTO": "tcp"}, "memory": null, "memory_swap": null, "name": "wordpress", "node": "/api/v1/node/fa9df19a-162b-45b4-bb5a-152dfd1b133f/", "public_dns": "wordpress-1.fa9df19a-tifayuki.node.docker.io", "resource_uri": "/api/v1/container/52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d/", "roles": [], "run_command": "/run.sh", "service": "/api/v1/service/81bbc30a-35de-4f5e-840d-87bc2573d818/", "started_datetime": "Wed, 1 Oct 2014 14:54:23 +0000", "state": "Stopping", "stopped_datetime": null, "unique_name": "wordpress-1", "uuid": "52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d"}'
        )
        mock_send.side_effect = [fake_resp(fake_container_fetch), fake_resp(fake_container_stop)]
        container = dockercloud.Container.fetch('52fffbca-88b2-4eac-a66d-8f8ca7e3ff2d')
        self.assertTrue(container.stop())
        result = json.loads(json.dumps(container.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)
