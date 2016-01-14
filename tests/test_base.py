from __future__ import absolute_import

import json
import unittest

import unittest.mock as mock

import dockercloud
from dockercloud.api.base import Restful, Mutable, Immutable


class RestfulTestCase(unittest.TestCase):
    def setUp(self):
        self.pk = Restful.pk
        Restful.pk = 'uuid'

    def tearDown(self):
        Restful.pk = self.pk

    def test_restful_init(self):
        model = Restful(key1='value1', key2='value2')
        self.assertEqual('value1', model.key1)
        self.assertEqual('value2', model.key2)

    def test_restful_setattr(self):
        model = Restful()

        setattr(model, 'key', 'value')
        self.assertEqual('value', model.key)
        self.assertEqual(['key'], model.__changedattrs__)

        setattr(model, 'key', 'other value')
        self.assertEqual('other value', model.key)
        self.assertEqual(['key'], model.__changedattrs__)

        setattr(model, 'another_key', 'another_value')
        self.assertEqual('another_value', model.another_key)
        self.assertEqual(['key', 'another_key'], model.__changedattrs__)

    def test_restful_getchanges(self):
        model = Restful()
        self.assertEqual([], model.__getchanges__())

        model.__changedattrs__ = ['dockercloud']
        self.assertEqual(['dockercloud'], model.__getchanges__())

    def test_restful_setchanges(self):
        model = Restful()
        model.__setchanges__('abc')
        self.assertEqual('abc', model.__changedattrs__)

        model.__setchanges__(None)
        self.assertIsNone(model.__changedattrs__)

    def test_restful_loaddict(self):
        model = Restful()
        self.assertRaises(AssertionError, model._loaddict, {'key': 'value'})

        model.endpoint = 'endpoint'
        model.subsystem = "subsystem"
        model._loaddict({'key': 'value'})
        self.assertEqual('value', model.key)
        self.assertEqual("/".join(["api", model.subsystem, model._api_version, model.endpoint.lstrip("/"), model.pk]),
                         model._detail_uri)
        self.assertEqual([], model.__getchanges__())

    def test_restful_pk(self):
        model = Restful()
        self.assertEqual(model.__class__._pk_key(), model.pk)

    def test_restful_is_dirty(self):
        model = Restful()
        self.assertFalse(model.is_dirty)

        model.key = 'value'
        self.assertTrue(model.is_dirty)

    @mock.patch('dockercloud.api.base.send_request')
    def test_restful_perform_action(self, mock_send_request):
        try:
            model = Restful()
            self.assertRaises(dockercloud.ApiError, model._perform_action, 'action')

            model.endpoint = 'fake'
            model.subsystem = "subsystem"
            model._detail_uri = "/".join(
                    ["api", model.subsystem, model._api_version, model.endpoint.lstrip("/"), model.pk])
            mock_send_request.side_effect = [{'key': 'value'}, None]
            self.assertTrue(model._perform_action('action', params={'k': 'v'}, data={'key': 'value'}))
            self.assertEqual('value', model.key)
            mock_send_request.assert_called_with('POST', "/".join([model._detail_uri, "action"]), data={'key': 'value'},
                                                 params={'k': 'v'})

            self.assertFalse(model._perform_action('action', {'key': 'value'}))

        finally:
            if hasattr(Restful, 'endpoint'):
                delattr(Restful, 'endpoint')

    @mock.patch('dockercloud.api.base.send_request')
    def test_restful_expand_attribute(self, mock_send_request):
        model = Restful()
        self.assertRaises(dockercloud.ApiError, model._expand_attribute, 'attribute')

        model._detail_uri = 'fake/uuid'
        mock_send_request.side_effect = [{'key': 'value'}, None]
        self.assertEqual('value', model._expand_attribute('key'))

        self.assertIsNone(model._expand_attribute('key'))

    def test_restful_get_all_attributes(self):
        model = Restful()
        model.key = 'value'
        self.assertDictEqual({'key': 'value'}, model.get_all_attributes())


class ImmutableTestCase(unittest.TestCase):
    def setUp(self):
        self.pk = Immutable.pk
        Immutable.pk = 'uuid'

    def tearDown(self):
        Immutable.pk = self.pk

    @mock.patch('dockercloud.api.base.send_request')
    def test_immutable_fetch(self, mock_send_request):
        self.assertRaises(AssertionError, Immutable.fetch, 'uuid')

        try:
            ret_json = {"key": "value"}
            mock_send_request.return_value = ret_json
            Immutable.endpoint = 'endpoint'
            Immutable.subsystem = "subsystem"
            model = Immutable.fetch('uuid')
            mock_send_request.assert_called_with('GET', 'api/subsystem/%s/endpoint/uuid' % Immutable._api_version)
            self.assertIsInstance(model, Immutable)
            self.assertEqual('value', model.key)
        finally:
            if hasattr(Immutable, 'endpoint'):
                delattr(Immutable, 'endpoint')

    @mock.patch('dockercloud.api.base.send_request')
    def test_immutable_list(self, mock_send_request):
        self.assertRaises(AssertionError, Immutable.list)
        try:
            kwargs = {'key': 'value'}
            ret_json = {"meta": {"limit": 25, "next": None, "offset": 0, "previous": None, "total_count": 1},
                        "objects": [{"key": "value1"}, {"key": "value2"}]}
            mock_send_request.return_value = ret_json
            Immutable.endpoint = 'fake'
            models = Immutable.list(**kwargs)
            mock_send_request.assert_called_with('GET', 'api/subsystem/%s/fake' % Immutable._api_version, params=kwargs)
            self.assertEqual(2, len(models))
            self.assertIsInstance(models[0], Immutable)
            self.assertEqual('value1', models[0].key)
            self.assertIsInstance(models[1], Immutable)
            self.assertEqual('value2', models[1].key)
        finally:
            if hasattr(Immutable, 'endpoint'):
                delattr(Immutable, 'endpoint')

    @mock.patch('dockercloud.api.base.send_request')
    def test_immutable_refresh(self, mock_send_request):
        try:
            model = Immutable()
            model.key = 'value'
            self.assertFalse(model.refresh(force=False))

            self.assertRaises(dockercloud.ApiError, model.refresh, force=True)

            Immutable.endpoint = 'endpoint'
            Immutable.subsystem = 'subsystem'
            model._detail_uri = 'api/subsystem/%s/endpoint/uuid' % Immutable._api_version
            mock_send_request.side_effect = [{'newkey': 'newvalue'}, None]
            self.assertTrue(model.refresh(force=True))
            self.assertEqual('newvalue', model.newkey)
            mock_send_request.assert_called_with('GET', model._detail_uri)

            self.assertFalse(model.refresh(force=True))
            mock_send_request.assert_called_with('GET', model._detail_uri)
        finally:
            if hasattr(Immutable, 'endpoint'):
                delattr(Immutable, 'endpoint')


class MutableTestCase(unittest.TestCase):
    def setUp(self):
        self.pk = Mutable.pk
        Mutable.pk = 'uuid'

    def tearDown(self):
        Mutable.pk = self.pk

    def test_mutable_create(self):
        self.assertIsInstance(Mutable.create(), Mutable)

    @mock.patch('dockercloud.api.base.send_request')
    def test_mutable_delete(self, mock_send_request):
        try:
            model = Mutable()
            self.assertRaises(dockercloud.ApiError, model.delete)

            Mutable.endpoint = 'fake'
            model._detail_uri = 'fake/uuid'
            mock_send_request.side_effect = [{'key': 'value'}, None]
            self.assertTrue(model.delete())
            self.assertEqual('value', model.key)
            mock_send_request.assert_called_with('DELETE', 'fake/uuid')

            self.assertTrue(model.delete())
            self.assertIsNone(model._detail_uri)
            self.assertFalse(model.is_dirty)
        finally:
            if hasattr(Mutable, 'endpoint'):
                delattr(Mutable, 'endpoint')

    @mock.patch('dockercloud.api.base.send_request')
    def test_mutable_save(self, mock_send_request):
        try:
            self.assertTrue(Mutable().save())

            model = Mutable()
            model.key = 'value'
            self.assertRaises(AssertionError, model.save)

            Mutable.endpoint = 'endpoint'
            Mutable.subsystem = 'subsystem'
            mock_send_request.return_value = None
            result = model.save()
            mock_send_request.assert_called_with('POST', 'api/subsystem/%s/endpoint' % Mutable._api_version,
                                                 data=json.dumps({'key': 'value'}))
            self.assertFalse(result)

            mock_send_request.return_value = {'newkey': 'newvalue'}
            result = model.save()
            mock_send_request.assert_called_with('POST', 'api/subsystem/%s/endpoint' % Mutable._api_version,
                                                 data=json.dumps({'key': 'value'}))
            self.assertTrue(result)
            self.assertEqual('newvalue', model.newkey)

            model.key = 'another value'
            mock_send_request.return_value = {'newkey2': 'newvalue2'}
            model._detail_uri = 'api/subsystem/%s/endpoint/uuid' % Immutable._api_version
            result = model.save()
            mock_send_request.assert_called_with('PATCH', 'api/subsystem/%s/endpoint/uuid' % Mutable._api_version,
                                                 data=json.dumps({'key': 'another value'}))
            self.assertTrue(result)
            self.assertEqual('another value', model.key)
            self.assertEqual('newvalue2', model.newkey2)
        finally:
            if hasattr(Mutable, 'endpoint'):
                delattr(Mutable, 'endpoint')
