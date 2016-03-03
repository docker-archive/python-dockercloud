from __future__ import absolute_import

import logging

from requests import Request, Session
from requests import utils
from urllib.parse import urljoin

import dockercloud
from .exceptions import ApiError, AuthError

logger = logging.getLogger("python-dockercloud")

global_session = Session()


def get_session():
    return global_session


def close_session():
    try:
        global global_session
        global_session.close()
    except:
        pass


def new_session():
    close_session()
    global global_session
    global_session = Session()


def send_request(method, path, inject_header=True, **kwargs):
    json = None
    url = urljoin(dockercloud.rest_host.rstrip("/"), path.strip("/").encode("ascii", "ignore"))
    if not url.endswith("/"):
        url = "%s/" % url
    user_agent = 'python-dockercloud/%s' % dockercloud.__version__
    if dockercloud.user_agent:
        user_agent = "%s %s" % (dockercloud.user_agent, user_agent)

    # construct headers
    headers = {'Content-Type': 'application/json', 'User-Agent': user_agent}
    headers.update(dockercloud.auth.get_auth_header())

    # construct request
    s = get_session()
    request = Request(method, url, headers=headers, **kwargs)
    # get environment proxies
    env_proxies = utils.get_environ_proxies(url) or {}
    kw_args = {'proxies': env_proxies}

    # make the request
    req = s.prepare_request(request)
    logger.info("Prepared Request: %s, %s, %s, %s" % (req.method, req.url, req.headers, kwargs))
    response = s.send(req, **kw_args)
    status_code = getattr(response, 'status_code', None)
    logger.info("Response: Status %s, %s, %s" % (str(status_code), response.headers, response.text))

    # handle the response
    if not status_code:
        # Most likely network trouble
        raise ApiError("No Response (%s %s)" % (method, url))
    elif 200 <= status_code <= 299:
        # Success
        if status_code != 204:
            # Try to parse the response.
            try:
                json = response.json()
                if response.headers and inject_header:
                    json["dockercloud_action_uri"] = response.headers.get("X-DockerCloud-Action-URI", "")
            except TypeError:
                raise ApiError("JSON Parse Error (%s %s). Response: %s" % (method, url, response.text))
        else:
            json = None
    else:
        # Server returned an error
        if status_code == 401:
            raise AuthError("Not authorized")
        else:
            raise ApiError("Status %s (%s %s). Response: %s" % (str(status_code), method, url, response.text))
    return json
