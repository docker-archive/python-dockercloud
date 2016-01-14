from __future__ import absolute_import

import unittest

import unittest.mock as mock

import dockercloud
from .fake_api import *


class ActionTestCase(unittest.TestCase):
    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_action_list(self, mock_send):
        attributes = json.loads(
                '[{"action": "Node Cluster Create", "end_date": "Mon, 29 Sep 2014 15:40:59 +0000", "ip": "207.41.188.212", "location": "New York, United States", "method": "POST", "object": "/api/v1/nodecluster/a02c3763-e639-46fc-a6db-587f4dbb5444/", "path": "/api/v1/nodecluster/", "resource_uri": "/api/v1/action/7f62b667-2693-420a-ad2e-41cda5605322/", "start_date": "Mon, 29 Sep 2014 15:40:59 +0000", "state": "Success", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36", "uuid": "7f62b667-2693-420a-ad2e-41cda5605322"}, ' \
                '{"action": "Node Cluster Deploy", "end_date": "Mon, 29 Sep 2014 15:41:01 +0000", "ip": "207.41.188.212", "location": "New York, United States", "method": "POST", "object": "/api/v1/nodecluster/a02c3763-e639-46fc-a6db-587f4dbb5444/", "path": "/api/v1/nodecluster/a02c3763-e639-46fc-a6db-587f4dbb5444/deploy/", "resource_uri": "/api/v1/action/db69b048-3bab-4a2e-bcbd-91265edf1a31/", "start_date": "Mon, 29 Sep 2014 15:41:00 +0000", "state": "Failed", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36", "uuid": "db69b048-3bab-4a2e-bcbd-91265edf1a31"}, ' \
                '{"action": "Node Deploy", "end_date": "Mon, 29 Sep 2014 15:41:16 +0000", "ip": "207.41.188.212", "location": "New York, United States", "method": "POST", "object": "/api/v1/node/fa9df19a-162b-45b4-bb5a-152dfd1b133f/", "path": "/api/v1/node/fa9df19a-162b-45b4-bb5a-152dfd1b133f/deploy/", "resource_uri": "/api/v1/action/ce9ae16b-88fa-4be6-b12e-fc970b8d2445/", "start_date": "Mon, 29 Sep 2014 15:41:16 +0000", "state": "Failed", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36", "uuid": "ce9ae16b-88fa-4be6-b12e-fc970b8d2445"}]'
        )
        mock_send.return_value = fake_resp(fake_action_list)
        actions = dockercloud.Action.list()
        for i in range(0, len(actions)):
            result = json.loads(json.dumps(actions[i].get_all_attributes()))
            target = json.loads(json.dumps(attributes[i]))
            self.assertDictEqual(target, result)

    @mock.patch.object(dockercloud.api.http.Session, 'send')
    def test_action_fetch(self, mock_send):
        attribute = json.loads(
                '{"action": "Node Cluster Create", "end_date": "Mon, 29 Sep 2014 15:40:59 +0000", "ip": "207.41.188.212", "location": "New York, United States", "logs": "", "method":"POST", "object": "/api/v1/nodecluster/a02c3763-e639-46fc-a6db-587f4dbb5444/", "path": "/api/v1/nodecluster/", "resource_uri": "/api/v1/action/7f62b667-2693-420a-ad2e-41cda5605322/", "start_date": "Mon, 29 Sep 2014 15:40:59 +0000", "state": "Success", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36", "uuid": "7f62b667-2693-420a-ad2e-41cda5605322"}'
        )
        mock_send.return_value = fake_resp(fake_action_fetch)
        action = dockercloud.Action.fetch("7f62b667-2693-420a-ad2e-41cda5605322")
        result = json.loads(json.dumps(action.get_all_attributes()))
        target = json.loads(json.dumps(attribute))
        self.assertDictEqual(target, result)
