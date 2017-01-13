from __future__ import absolute_import

import base64
import json
import os
import subprocess

from requests.auth import HTTPBasicAuth

import dockercloud
from .http import send_request

HUB_INDEX = "https://index.docker.io/v1/"


def authenticate(username, password):
    verify_credential(username, password)
    dockercloud.basic_auth = base64.b64encode("%s:%s" % (username, password))


def verify_credential(username, password):
    auth = HTTPBasicAuth(username, password)
    send_request("GET", "/auth", auth=auth)


def is_authenticated():
    try:
        dockercloud.basic_auth = base64.b64encode("%s:%s" % (dockercloud.user, dockercloud.password))
    except:
        pass

    try:
        dockercloud.basic_auth = base64.b64encode("%s:%s" % (dockercloud.user, dockercloud.apikey))
    except:
        pass

    return dockercloud.dockercloud_auth or dockercloud.basic_auth


def logout():
    dockercloud.dockercloud_auth = None
    dockercloud.basic_auth = None


def load_from_file(f="~/.docker/config.json"):
    try:
        with open(os.path.expanduser(f)) as config_file:
            data = json.load(config_file)
    except:
        return None

    creds_store = data.get("credsStore", None)
    if creds_store:
        try:
            cmd = "docker-credential-" + creds_store
            p = subprocess.Popen([cmd, 'get'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = p.communicate(input=HUB_INDEX)[0]
        except:
            raise dockercloud.AuthError(
                'error getting credentials - err: exec: "%s": executable file not found in $PATH, out: ``' % cmd)

        try:
            credential = json.loads(out)
            username = credential.get("Username")
            password = credential.get("Secret")
            return base64.b64encode("%s:%s" % (username, password))
        except:
            return None

    else:
        return data.get("auths", {}).get(HUB_INDEX, {}).get("auth", None)


def get_auth_header():
    try:
        dockercloud.basic_auth = base64.b64encode("%s:%s" % (dockercloud.user, dockercloud.password))
    except:
        pass

    try:
        dockercloud.basic_auth = base64.b64encode("%s:%s" % (dockercloud.user, dockercloud.apikey))
    except:
        pass

    if dockercloud.dockercloud_auth:
        return {'Authorization': dockercloud.dockercloud_auth}
    if dockercloud.basic_auth:
        return {'Authorization': 'Basic %s' % dockercloud.basic_auth}
    return {}
