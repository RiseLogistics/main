import requests
import json
from uuid import uuid4

from ..models.response import Response
from ..models.error import Error
from .exceptions import (
    LeafLinkClientRequestError,
    LeafLinkClient5XXError
)
from structlog import get_logger


def logger():
    _r = "[LeafLink - {0}]".format(str(uuid4())[-12:])
    _l = get_logger()
    return _l.bind(REQUEST=_r)


class _Base(object):
    """
        https://leaflink.com/api/docs#/
    """

    def __init__(self, requests_client=None, user_configs=None):
        self.defaults = dict(
            BASE_URL=None,
            API_KEY=None,
            HEADERS={"content-type": "application/json",
                     "User-Agent": "DYME"}
        )

        if isinstance(user_configs, dict):
            self.defaults.update(user_configs)

        self.req_client = requests_client or requests
        self._log = None

    def log(self, msg, context, headers=None, is_error=False):
        if not self._log:
            self._log = logger()
        try:
            msg = str(msg)
            msg_key = "[{1}]".format("", context)
            try:
                if "APIResource." in msg:
                    loc = msg.find("APIResource.")
                    end = len("APIResource.") + loc + 5

                    msg = msg[loc:end].upper()
                    if msg[-1:] not in [" ", "H", "T", "E"]: msg = msg[:-1]

            except: pass

            if is_error:
                if headers:
                    headers["Authorization"] = "****" + headers["Authorization"][-12:]
                    self._log.error("EXCEPTION - " + msg_key,
                                    CONTEXT=msg,
                                    HEADERS=headers,
                                    DATA=self.data)
                else:
                    self._log.error("EXCEPTION - " + msg_key,
                                    CONTEXT=msg,
                                    DATA=self.data)

            else: self._log.info(msg_key, CONTEXT=msg)

        except:
            self._log.error("failed to format log msg text")


class _Client(_Base):
    def __init__(self, user_configs=None):
        _Base.__init__(self, user_configs=user_configs)

    def get(self, url=None, raw_response=False):
        r = self._request(url or self.url, self.get)
        return self._validate_response(r, raw_response)

    def post(self, raw_response=False):
        r = self._request(self.url, self.post, data=self.data)
        return self._validate_response(r, raw_response)

    def put(self, raw_response=False):
        r = self._request(self.url, self.put, self.data)
        return self._validate_response(r, raw_response)

    def patch(self, raw_response=False):
        r = self._request(self.url, self.patch, self.data)
        return self._validate_response(r, raw_response)

    def delete(self, raw_response=False):
        r = self._request(self.url, self.delete)
        return self._validate_response(r, raw_response)

    def attachment(self, raw_response=False):
        r = self._request(self.url, self.attachment, self.data)
        return self._validate_response(r, raw_response)

    def _request(self, url, method, data=None, headers=None):
        self.log(method, (url))

        r = None
        self.defaults["HEADERS"]["Authorization"] = "Token " + self.auth

        req_args= dict(
            headers=self.defaults["HEADERS"],
            params=self.get_params
        )

        if method == self.get:
            r = self.req_client.get(url, **req_args)

        elif method == self.post:
            r = self.req_client.post(url, json=data, **req_args)

        elif method == self.put:
            r = self.req_client.put(url, json=data, **req_args)

        elif method == self.patch:
            r = self.req_client.patch(url, json=data, **req_args)

        elif method == self.delete:
            r = self.req_client.delete(url, **req_args)

        elif method == self.attachment:
            req_args["headers"]["content-type"] = "multipart/form-data"
            r = self.req_client.post(url, files=data, **req_args)

        return r

    def _validate_response(self, r, raw_response):

        if 200 > r.status_code or r.status_code >= 300:
            _msg =("[{r.url}] - "
                   "STATUS_CODE[{r.status_code}]".format(r=r))

            self.log("LeafLinkClientRequestError",
                     r.url, headers=self.defaults["HEADERS"],
                     is_error=True)

            self.log("LeafLinkClientRequestError",
                     r.content,
                     headers=r.request.headers,
                     is_error=True)

            try: res = json.load(r)
            except: res = dict(detail = r.content)

            res["status_code"] = r.status_code

            response = Error().load(res)
            error_payload = dict(err_response=response,
                                 expr=r.status_code,
                                 msg=_msg)

            self.log("Error Info", str(error_payload)
                     + " - " + str(_msg) + " / " + str(res["detail"]))

            # if r.status_code >= 500:
            #     raise LeafLinkClient5XXError(**error_payload)

            raise LeafLinkClientRequestError(**error_payload)

        content = dict()

        if raw_response:
            content = r.content

        elif r.content not in ["", None]:
            content = json.loads(r.content.decode("utf-8"))
            if not isinstance(content, dict):
                content = dict(results=content)

            content["status_code"] = r.status_code

        else:
            content = dict(
                results=content,
                status_code=r.status_code,
                next=None,
                previous=None
            )

        return Response().load(self._build_pagination(content))

    def _build_pagination(self, _request):
        if "next" in _request and _request["next"]:
            next_resource = _request["next"]
            _request["next"] = lambda : self.get(url=next_resource)

        else: _request["next"] = None

        if "previous" in _request and _request["previous"]:
            previous_resource = _request["previous"]
            _request["previous"] = lambda : self.get(url=previous_resource)

        else: _request["previous"] = None

        return _request

    @property
    def url(self):
        raise NotImplementedError

    @property
    def auth(self):
        raise NotImplementedError


class APIResource(_Client):
    CLS_ENDPOINT = None

    def __init__(self, endpoint=None,
                 data=None, query=None,
                 path_params=None,  user_configs=None):

        _Client.__init__(self, user_configs)

        self.data = data
        self.params = query
        self.path_params = path_params

        if endpoint:
            self.CLS_ENDPOINT = endpoint

    @property
    def endpoint(self):
        return self.CLS_ENDPOINT

    @property
    def get_params(self):
        if not self.params:
            return {}

        return self.params

    @property
    def url(self):
        if not self.endpoint:
            raise Exception("LeafLink API resource endpoint not set")

        return self._build_url()

    @property
    def auth(self):
        return self.defaults["API_KEY"]

    def _build_url(self):
        url = self.defaults["BASE_URL"]

        if self.path_params:
            return url + self.endpoint.format(self.path_params)

        return url + self.endpoint
