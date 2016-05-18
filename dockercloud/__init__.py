import base64
import logging
import os

import requests
from future.standard_library import install_aliases

install_aliases()

from dockercloud.api import auth
from dockercloud.api.service import Service
from dockercloud.api.container import Container
from dockercloud.api.repository import Repository
from dockercloud.api.node import Node
from dockercloud.api.action import Action
from dockercloud.api.nodecluster import NodeCluster
from dockercloud.api.nodetype import NodeType
from dockercloud.api.nodeprovider import Provider
from dockercloud.api.noderegion import Region
from dockercloud.api.tag import Tag
from dockercloud.api.trigger import Trigger
from dockercloud.api.stack import Stack
from dockercloud.api.exceptions import ApiError, AuthError, ObjectNotFound, NonUniqueIdentifier
from dockercloud.api.utils import Utils
from dockercloud.api.events import Events
from dockercloud.api.nodeaz import AZ

__version__ = '1.0.5'

dockercloud_auth = os.environ.get('DOCKERCLOUD_AUTH')
basic_auth = auth.load_from_file("~/.docker/config.json")

if os.environ.get('DOCKERCLOUD_USER') and os.environ.get('DOCKERCLOUD_PASS'):
    basic_auth = base64.b64encode("%s:%s" % (os.environ.get('DOCKERCLOUD_USER'), os.environ.get('DOCKERCLOUD_PASS')))
if os.environ.get('DOCKERCLOUD_USER') and os.environ.get('DOCKERCLOUD_APIKEY'):
    basic_auth = base64.b64encode("%s:%s" % (os.environ.get('DOCKERCLOUD_USER'), os.environ.get('DOCKERCLOUD_APIKEY')))

rest_host = os.environ.get("DOCKERCLOUD_REST_HOST") or 'https://cloud.docker.com/'
stream_host = os.environ.get("DOCKERCLOUD_STREAM_HOST") or 'wss://ws.cloud.docker.com/'

user_agent = None

logging.basicConfig()
logger = logging.getLogger("python-dockercloud")

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
