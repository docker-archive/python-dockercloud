import unittest

try:
    import mock
except ImportError:
    import unittest.mock as mock

import dockercloud
from dockercloud.api.exceptions import ObjectNotFound, ApiError, NonUniqueIdentifier


class FetchRemoteObjectTestCase(unittest.TestCase):
    @mock.patch('dockercloud.Container.list')
    @mock.patch('dockercloud.Container.fetch')
    def test_fetch_remote_container(self, mock_fetch, mock_list):
        # test container exist queried with uuid4
        mock_fetch.return_value = 'returned'
        self.assertEqual(dockercloud.Utils.fetch_remote_container('7A4CFE51-03BB-42D6-825E-3B533888D8CD', True),
                         'returned')
        self.assertEqual(dockercloud.Utils.fetch_remote_container('7A4CFE51-03BB-42D6-825E-3B533888D8CD', False),
                         'returned')

        # test container doesn't exist queried with uuid4
        mock_fetch.side_effect = ObjectNotFound
        self.assertRaises(ObjectNotFound, dockercloud.Utils.fetch_remote_container,
                          '7A4CFE51-03BB-42D6-825E-3B533888D8CD',
                          True)
        self.assertIsInstance(dockercloud.Utils.fetch_remote_container('7A4CFE51-03BB-42D6-825E-3B533888D8CD', False),
                              ObjectNotFound)

        # test unique container found queried with short uuid
        container = dockercloud.Container.create()
        container.uuid = 'uuid'
        mock_list.side_effect = [[container], []]
        mock_fetch.side_effect = [container]
        self.assertEquals(dockercloud.Utils.fetch_remote_container('shortuuid', True), container)
        mock_list.side_effect = [[container], []]
        mock_fetch.side_effect = [container]
        self.assertEquals(dockercloud.Utils.fetch_remote_container('shortuuid', False), container)

        # test unique container found queried with name
        mock_list.side_effect = [[], [container]]
        mock_fetch.side_effect = [container]
        self.assertEquals(dockercloud.Utils.fetch_remote_container('name', True), container)
        mock_list.side_effect = [[], [container]]
        mock_fetch.side_effect = [container]
        self.assertEquals(dockercloud.Utils.fetch_remote_container('name', False), container)

        # test no container found
        mock_list.side_effect = [[], []]
        self.assertRaises(ObjectNotFound, dockercloud.Utils.fetch_remote_container, 'uuid_or_name', True)
        mock_list.side_effect = [[], []]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_container('uuid_or_name', False), ObjectNotFound)

        # test multi-container found
        mock_list.side_effect = [['container1', 'container2'], []]
        self.assertRaises(NonUniqueIdentifier, dockercloud.Utils.fetch_remote_container, 'uuid_or_name', True)
        mock_list.side_effect = [['container1', 'container2'], []]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_container('uuid_or_name', False), NonUniqueIdentifier)
        mock_list.side_effect = [[], ['container1', 'container2']]
        self.assertRaises(NonUniqueIdentifier, dockercloud.Utils.fetch_remote_container, 'uuid_or_name', True)
        mock_list.side_effect = [[], ['container1', 'container2']]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_container('uuid_or_name', False), NonUniqueIdentifier)

        # test api error
        mock_list.side_effect = [ApiError, ApiError]
        self.assertRaises(ApiError, dockercloud.Utils.fetch_remote_container, 'uuid_or_name', True)
        self.assertRaises(ApiError, dockercloud.Utils.fetch_remote_container, 'uuid_or_name', False)

    @mock.patch('dockercloud.Service.list')
    @mock.patch('dockercloud.Service.fetch')
    def test_fetch_remote_service(self, mock_fetch, mock_list):
        # test cluster exist queried with uuid4
        mock_fetch.return_value = 'returned'
        self.assertEqual(dockercloud.Utils.fetch_remote_service('7A4CFE51-03BB-42D6-825E-3B533888D8CD', True),
                         'returned')
        self.assertEqual(dockercloud.Utils.fetch_remote_service('7A4CFE51-03BB-42D6-825E-3B533888D8CD', False),
                         'returned')

        # test cluster doesn't exist queried with uuid4
        mock_fetch.side_effect = ObjectNotFound
        self.assertRaises(ObjectNotFound, dockercloud.Utils.fetch_remote_service,
                          '7A4CFE51-03BB-42D6-825E-3B533888D8CD',
                          True)
        self.assertIsInstance(dockercloud.Utils.fetch_remote_service('7A4CFE51-03BB-42D6-825E-3B533888D8CD', False),
                              ObjectNotFound)

        # test unique cluster found queried with short uuid
        service = dockercloud.Service.create()
        service.uuid = 'uuid'
        mock_list.side_effect = [[service], []]
        mock_fetch.side_effect = [service]
        self.assertEquals(dockercloud.Utils.fetch_remote_service('shortuuid', True), service)
        mock_list.side_effect = [[service], []]
        mock_fetch.side_effect = [service]
        self.assertEquals(dockercloud.Utils.fetch_remote_service('shortuuid', False), service)

        # test unique cluster found queried with name
        mock_list.side_effect = [[], [service]]
        mock_fetch.side_effect = [service]
        self.assertEquals(dockercloud.Utils.fetch_remote_service('name', True), service)
        mock_list.side_effect = [[], [service]]
        mock_fetch.side_effect = [service]
        self.assertEquals(dockercloud.Utils.fetch_remote_service('name', False), service)

        # test no cluster found
        mock_list.side_effect = [[], []]
        self.assertRaises(ObjectNotFound, dockercloud.Utils.fetch_remote_service, 'uuid_or_name', True)
        mock_list.side_effect = [[], []]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_service('uuid_or_name', False), ObjectNotFound)

        # test multi-cluster found
        mock_list.side_effect = [['cluster1', 'cluster2'], []]
        self.assertRaises(NonUniqueIdentifier, dockercloud.Utils.fetch_remote_service, 'uuid_or_name', True)
        mock_list.side_effect = [['cluster1', 'cluster2'], []]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_service('uuid_or_name', False), NonUniqueIdentifier)
        mock_list.side_effect = [[], ['cluster1', 'cluster2']]
        self.assertRaises(NonUniqueIdentifier, dockercloud.Utils.fetch_remote_service, 'uuid_or_name', True)
        mock_list.side_effect = [[], ['cluster1', 'cluster2']]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_service('uuid_or_name', False), NonUniqueIdentifier)

        # test api error
        mock_list.side_effect = [ApiError, ApiError]
        self.assertRaises(ApiError, dockercloud.Utils.fetch_remote_service, 'uuid_or_name', True)
        self.assertRaises(ApiError, dockercloud.Utils.fetch_remote_service, 'uuid_or_name', False)

    @mock.patch('dockercloud.Node.list')
    @mock.patch('dockercloud.Node.fetch')
    def test_fetch_remote_node(self, mock_fetch, mock_list):
        # test node exist queried with uuid4
        mock_fetch.return_value = 'returned'
        self.assertEqual(dockercloud.Utils.fetch_remote_node('7A4CFE51-03BB-42D6-825E-3B533888D8CD', True), 'returned')
        self.assertEqual(dockercloud.Utils.fetch_remote_node('7A4CFE51-03BB-42D6-825E-3B533888D8CD', False), 'returned')

        # test node doesn't exist queried with uuid4
        mock_fetch.side_effect = ObjectNotFound
        self.assertRaises(ObjectNotFound, dockercloud.Utils.fetch_remote_node, '7A4CFE51-03BB-42D6-825E-3B533888D8CD',
                          True)
        self.assertIsInstance(dockercloud.Utils.fetch_remote_node('7A4CFE51-03BB-42D6-825E-3B533888D8CD', False),
                              ObjectNotFound)

        # test unique node found queried with short uuid
        node = dockercloud.Node.create()
        node.uuid = 'uuid'
        mock_list.side_effect = [[node]]
        mock_fetch.side_effect = [node]
        self.assertEquals(dockercloud.Utils.fetch_remote_node('uuid', True), node)
        mock_list.side_effect = [[node]]
        mock_fetch.side_effect = [node]
        self.assertEquals(dockercloud.Utils.fetch_remote_node('uuid', False), node)

        # test no node found
        mock_list.side_effect = [[]]
        self.assertRaises(ObjectNotFound, dockercloud.Utils.fetch_remote_node, 'uuid', True)
        mock_list.side_effect = [[]]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_node('uuid', False), ObjectNotFound)

        # test multi-node found
        mock_list.side_effect = [['node1', 'node2']]
        self.assertRaises(NonUniqueIdentifier, dockercloud.Utils.fetch_remote_node, 'uuid', True)
        mock_list.side_effect = [['node1', 'node2']]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_node('uuid', False), NonUniqueIdentifier)

        # test api error
        mock_list.side_effect = [ApiError, ApiError]
        self.assertRaises(ApiError, dockercloud.Utils.fetch_remote_node, 'uuid', True)
        self.assertRaises(ApiError, dockercloud.Utils.fetch_remote_node, 'uuid', False)

    @mock.patch('dockercloud.NodeCluster.list')
    @mock.patch('dockercloud.NodeCluster.fetch')
    def test_fetch_remote_nodecluster(self, mock_fetch, mock_list):
        # test nodecluster exist queried with uuid4
        mock_fetch.return_value = 'returned'
        self.assertEqual(dockercloud.Utils.fetch_remote_nodecluster('7A4CFE51-03BB-42D6-825E-3B533888D8CD', True),
                         'returned')
        self.assertEqual(dockercloud.Utils.fetch_remote_nodecluster('7A4CFE51-03BB-42D6-825E-3B533888D8CD', False),
                         'returned')

        # test nodecluster doesn't exist queried with uuid4
        mock_fetch.side_effect = ObjectNotFound
        self.assertRaises(ObjectNotFound, dockercloud.Utils.fetch_remote_nodecluster,
                          '7A4CFE51-03BB-42D6-825E-3B533888D8CD',
                          True)
        self.assertIsInstance(dockercloud.Utils.fetch_remote_nodecluster('7A4CFE51-03BB-42D6-825E-3B533888D8CD', False),
                              ObjectNotFound)

        # test unique nodecluster found queried with short uuid
        nodecluster = dockercloud.NodeCluster.create()
        nodecluster.uuid = 'uuid'
        mock_list.side_effect = [[nodecluster], []]
        mock_fetch.side_effect = [nodecluster]
        self.assertEquals(dockercloud.Utils.fetch_remote_nodecluster('shortuuid', True), nodecluster)
        mock_list.side_effect = [[nodecluster], []]
        mock_fetch.side_effect = [nodecluster]
        self.assertEquals(dockercloud.Utils.fetch_remote_nodecluster('shortuuid', False), nodecluster)

        # test unique nodecluster found queried with name
        mock_list.side_effect = [[], [nodecluster]]
        mock_fetch.side_effect = [nodecluster]
        self.assertEquals(dockercloud.Utils.fetch_remote_nodecluster('name', True), nodecluster)
        mock_list.side_effect = [[], [nodecluster]]
        mock_fetch.side_effect = [nodecluster]
        self.assertEquals(dockercloud.Utils.fetch_remote_nodecluster('name', False), nodecluster)

        # test no nodecluster found
        mock_list.side_effect = [[], []]
        self.assertRaises(ObjectNotFound, dockercloud.Utils.fetch_remote_nodecluster, 'uuid_or_name', True)
        mock_list.side_effect = [[], []]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_nodecluster('uuid_or_name', False), ObjectNotFound)

        # test multi-nodecluster found
        mock_list.side_effect = [['nodecluster1', 'nodecluster2'], []]
        self.assertRaises(NonUniqueIdentifier, dockercloud.Utils.fetch_remote_nodecluster, 'uuid_or_name', True)
        mock_list.side_effect = [['nodecluster1', 'nodecluster2'], []]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_nodecluster('uuid_or_name', False), NonUniqueIdentifier)
        mock_list.side_effect = [[], ['nodecluster1', 'nodecluster2']]
        self.assertRaises(NonUniqueIdentifier, dockercloud.Utils.fetch_remote_nodecluster, 'uuid_or_name', True)
        mock_list.side_effect = [[], ['nodecluster1', 'nodecluster2']]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_nodecluster('uuid_or_name', False), NonUniqueIdentifier)

        # test api error
        mock_list.side_effect = [ApiError, ApiError]
        self.assertRaises(ApiError, dockercloud.Utils.fetch_remote_nodecluster, 'uuid_or_name', True)
        self.assertRaises(ApiError, dockercloud.Utils.fetch_remote_nodecluster, 'uuid_or_name', False)

    @mock.patch('dockercloud.Swarm.list')
    @mock.patch('dockercloud.Swarm.fetch')
    def test_fetch_remote_swarm(self, mock_fetch, mock_list):
        # test the identifier w/ and w/o namespace
        mock_fetch.return_value = 'returned'
        self.assertEqual(dockercloud.Utils.fetch_remote_swarm('abc', True), 'returned')
        mock_fetch.assert_called_with("abc", namespace="")

        self.assertEqual(dockercloud.Utils.fetch_remote_swarm('tifayuki/abc', True), 'returned')
        mock_fetch.assert_called_with("abc", namespace="tifayuki")

        self.assertEqual(dockercloud.Utils.fetch_remote_swarm('tifayuki/abc/xyz', True), 'returned')
        mock_fetch.assert_called_with("abc/xyz", namespace="tifayuki")

        # test no swarm found
        mock_fetch.side_effect = ObjectNotFound
        self.assertRaises(ObjectNotFound, dockercloud.Utils.fetch_remote_swarm, 'swarm_id', True)
        self.assertIsInstance(dockercloud.Utils.fetch_remote_swarm('swarm_id', False), ObjectNotFound)

        # test multi-swarm found
        mock_fetch.return_value = 'returned'
        mock_list.side_effect = [['swarm1', 'swarm2'], []]
        self.assertRaises(NonUniqueIdentifier, dockercloud.Utils.fetch_remote_swarm, 'swarm_id', True)
        mock_list.side_effect = [['swarm1', 'swarm2'], []]
        self.assertIsInstance(dockercloud.Utils.fetch_remote_swarm('swarm_id', False), NonUniqueIdentifier)

        # test api error
        mock_list.side_effect = [ApiError, ApiError]
        self.assertRaises(ApiError, dockercloud.Utils.fetch_remote_swarm, 'swarm_id', True)
        self.assertRaises(ApiError, dockercloud.Utils.fetch_remote_swarm, 'swarm_id', False)
