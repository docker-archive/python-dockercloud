from __future__ import absolute_import

import re

from .action import Action
from .container import Container
from .exceptions import ApiError, ObjectNotFound, NonUniqueIdentifier
from .node import Node
from .nodecluster import NodeCluster
from .service import Service
from .stack import Stack


def is_uuid4(identifier):
    uuid4_regexp = re.compile('^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}', re.I)
    match = uuid4_regexp.match(identifier)
    return bool(match)


class Utils:
    @staticmethod
    def fetch_by_resource_uri(uri):
        if not isinstance(uri, basestring):
            raise ApiError("Uri format is invalid")
        terms = uri.strip("/").split("/")
        if len(terms) < 2:
            raise ApiError("Uri format is invalid")

        id = terms[-1]
        resource_type = terms[-2]

        if resource_type.lower() == "container":
            return Container.fetch(id)
        elif resource_type.lower() == "service":
            return Service.fetch(id)
        elif resource_type.lower() == "stack":
            return Stack.fetch(id)
        elif resource_type.lower() == "node":
            return Node.fetch(id)
        elif resource_type.lower() == "nodecluster":
            return NodeCluster.fetch(id)
        elif resource_type.lower() == "action":
            return Action.fetch(id)
        else:
            raise ApiError(
                    "Unsupported resource type. Only support: action, container, node, nodecluster, service, stack")

    @staticmethod
    def fetch_remote_container(identifier, raise_exceptions=True):
        try:
            if is_uuid4(identifier):
                try:
                    return Container.fetch(identifier)
                except Exception:
                    raise ObjectNotFound("Cannot find a container with the identifier '%s'" % identifier)
            else:
                if "." in identifier:
                    terms = identifier.split(".", 2)
                    objects_same_identifier = Container.list(name=terms[0], service__stack__name=terms[1])
                else:
                    objects_same_identifier = Container.list(uuid__startswith=identifier) or \
                                              Container.list(name=identifier)

                if len(objects_same_identifier) == 1:
                    uuid = objects_same_identifier[0].uuid
                    return Container.fetch(uuid)
                elif len(objects_same_identifier) == 0:
                    raise ObjectNotFound("Cannot find a container with the identifier '%s'" % identifier)
                raise NonUniqueIdentifier("More than one container has the same identifier, please use the long uuid")

        except (NonUniqueIdentifier, ObjectNotFound) as e:
            if not raise_exceptions:
                return e
            raise e

    @staticmethod
    def fetch_remote_service(identifier, raise_exceptions=True):
        try:
            if is_uuid4(identifier):
                try:
                    return Service.fetch(identifier)
                except Exception:
                    raise ObjectNotFound("Cannot find a service with the identifier '%s'" % identifier)
            else:
                if "." in identifier:
                    terms = identifier.split(".", 2)
                    objects_same_identifier = Service.list(name=terms[0], stack__name=terms[1])
                else:
                    objects_same_identifier = Service.list(uuid__startswith=identifier) or \
                                              Service.list(name=identifier)

                if len(objects_same_identifier) == 1:
                    uuid = objects_same_identifier[0].uuid
                    return Service.fetch(uuid)
                elif len(objects_same_identifier) == 0:
                    raise ObjectNotFound("Cannot find a service with the identifier '%s'" % identifier)
                raise NonUniqueIdentifier("More than one service has the same identifier, please use the long uuid")
        except (NonUniqueIdentifier, ObjectNotFound) as e:
            if not raise_exceptions:
                return e
            raise e

    @staticmethod
    def fetch_remote_stack(identifier, raise_exceptions=True):
        try:
            if is_uuid4(identifier):
                try:
                    return Stack.fetch(identifier)
                except Exception:
                    raise ObjectNotFound("Cannot find a stack with the identifier '%s'" % identifier)
            else:
                objects_same_identifier = Stack.list(uuid__startswith=identifier) or \
                                          Stack.list(name=identifier)
                if len(objects_same_identifier) == 1:
                    uuid = objects_same_identifier[0].uuid
                    return Stack.fetch(uuid)
                elif len(objects_same_identifier) == 0:
                    raise ObjectNotFound("Cannot find a stack with the identifier '%s'" % identifier)
                raise NonUniqueIdentifier("More than one stack has the same identifier, please use the long uuid")

        except (NonUniqueIdentifier, ObjectNotFound) as e:
            if not raise_exceptions:
                return e
            raise e

    @staticmethod
    def fetch_remote_node(identifier, raise_exceptions=True):
        try:
            if is_uuid4(identifier):
                try:
                    return Node.fetch(identifier)
                except Exception:
                    raise ObjectNotFound("Cannot find a node with the identifier '%s'" % identifier)
            else:
                objects_same_identifier = Node.list(uuid__startswith=identifier)
                if len(objects_same_identifier) == 1:
                    uuid = objects_same_identifier[0].uuid
                    return Node.fetch(uuid)
                elif len(objects_same_identifier) == 0:
                    raise ObjectNotFound("Cannot find a node with the identifier '%s'" % identifier)
                raise NonUniqueIdentifier("More than one node has the same identifier, please use the long uuid")

        except (NonUniqueIdentifier, ObjectNotFound) as e:
            if not raise_exceptions:
                return e
            raise e

    @staticmethod
    def fetch_remote_nodecluster(identifier, raise_exceptions=True):
        try:
            if is_uuid4(identifier):
                try:
                    return NodeCluster.fetch(identifier)
                except Exception:
                    raise ObjectNotFound("Cannot find a node cluster with the identifier '%s'" % identifier)
            else:
                objects_same_identifier = NodeCluster.list(uuid__startswith=identifier) or \
                                          NodeCluster.list(name=identifier)
                if len(objects_same_identifier) == 1:
                    uuid = objects_same_identifier[0].uuid
                    return NodeCluster.fetch(uuid)
                elif len(objects_same_identifier) == 0:
                    raise ObjectNotFound("Cannot find a node cluster with the identifier '%s'" % identifier)
                raise NonUniqueIdentifier(
                        "More than one node cluster has the same identifier, please use the long uuid")

        except (NonUniqueIdentifier, ObjectNotFound) as e:
            if not raise_exceptions:
                return e
            raise e

    @staticmethod
    def fetch_remote_action(identifier, raise_exceptions=True):
        try:
            if is_uuid4(identifier):
                try:
                    return Action.fetch(identifier)
                except Exception:
                    raise ObjectNotFound("Cannot find an action with the identifier '%s'" % identifier)
            else:
                objects_same_identifier = Action.list(uuid__startswith=identifier)
                if len(objects_same_identifier) == 1:
                    uuid = objects_same_identifier[0].uuid
                    return Action.fetch(uuid)
                elif len(objects_same_identifier) == 0:
                    raise ObjectNotFound("Cannot find an action cluster with the identifier '%s'" % identifier)
                raise NonUniqueIdentifier(
                        "More than one action has the same identifier, please use the long uuid")

        except (NonUniqueIdentifier, ObjectNotFound) as e:
            if not raise_exceptions:
                return e
            raise e
