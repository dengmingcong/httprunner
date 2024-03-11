import json
import time
from datetime import datetime, timedelta, timezone
from typing import NoReturn

import requests
import urllib3
from loguru import logger
from requests import Request, Response
from requests.exceptions import (
    InvalidSchema,
    InvalidURL,
    MissingSchema,
    RequestException,
)
from requests.structures import CaseInsensitiveDict

from httprunner.builtin import expand_nested_json
from httprunner.builtin.dictionary import get_sub_dict
from httprunner.models import RequestData, ResponseData
from httprunner.models import SessionData, ReqRespData
from httprunner.utils import lower_dict_keys, omit_long_data

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiResponse(Response):
    def raise_for_status(self):
        if hasattr(self, "error") and self.error:
            raise self.error
        Response.raise_for_status(self)


class MockResponse(Response):
    def __init__(self, content, headers, status_code):
        super().__init__()
        self.status_code = status_code
        self.headers = CaseInsensitiveDict(headers)
        self._content = content

    def raise_for_status(self):
        if hasattr(self, "error") and self.error:
            raise self.error
        Response.raise_for_status(self)

    def json(self):
        return self._content


def get_req_resp_record(requests_response: Response, **kwargs) -> ReqRespData:
    """get request and response info from Response() object."""

    def log_print(req_or_resp, r_type):
        msg = f"\n================== {r_type} details ==================\n"
        for key, value in req_or_resp.model_dump().items():
            if isinstance(value, dict):
                value = json.dumps(value, indent=4)

            msg += "{:<8} : {}\n".format(key, value)
        logger.debug(msg)

    # record actual request info
    request_headers = dict(requests_response.request.headers)
    request_cookies = requests_response.request._cookies.get_dict()

    request_body = requests_response.request.body
    if request_body is not None:
        try:
            # try to convert request body to json format
            request_body = json.loads(request_body)
        except json.JSONDecodeError:
            # str: a=1&b=2
            request_body = repr(request_body)
        except UnicodeDecodeError:
            # bytes/bytearray: request body in protobuf
            request_body = repr(request_body)
        except TypeError:
            # neither str nor bytes/bytearray, e.g. <MultipartEncoder>, <_io.BufferedReader>
            request_body = repr(request_body)

    request_data = RequestData(
        method=requests_response.request.method,
        url=requests_response.request.url,
        headers=request_headers,
        cookies=request_cookies,
        body=request_body,
    )

    # log request details in debug mode
    log_print(request_data, "request")

    # record response info
    resp_headers = dict(requests_response.headers)
    lower_resp_headers = lower_dict_keys(resp_headers)
    content_type = lower_resp_headers.get("content-type", "")

    if "image" in content_type:
        # response is image type, record bytes content only
        response_body = requests_response.content
    else:
        try:
            # try to record json data
            response_body = requests_response.json()
            if kwargs.get("is_expand_nested_json"):
                expand_nested_json(response_body)
        except ValueError:
            # only record at most 512 text charactors
            resp_text = requests_response.text
            response_body = omit_long_data(resp_text)

    response_data = ResponseData(
        status_code=requests_response.status_code,
        cookies=requests_response.cookies or {},
        encoding=requests_response.encoding,
        headers=resp_headers,
        content_type=content_type,
        body=response_body,
    )

    # log response details in debug mode
    log_print(response_data, "response")

    req_resp_data = ReqRespData(request=request_data, response=response_data)
    return req_resp_data


class HttpSession(requests.Session):
    """
    Class for performing HTTP requests and holding (session-) cookies between requests (in order
    to be able to log in and out of websites). Each request is logged so that HttpRunner can
    display statistics.

    This is a slightly extended version of `python-request <http://python-requests.org>`_'s
    :py:class:`requests.Session` class and mostly this class works exactly the same.
    """

    def __init__(self):
        super(HttpSession, self).__init__()
        self.data = SessionData()

    def update_last_req_resp_record(self, requests_response: Response) -> NoReturn:
        """
        update request and response info from Response() object.
        """
        # TODO: fix
        self.data.req_resps.pop()
        self.data.req_resps.append(get_req_resp_record(requests_response))

    def request(self, method, url, name=None, **kwargs) -> Response:
        """
        Constructs and sends a :py:class:`requests.Request`.
        Returns :py:class:`requests.Response` object.

        :param method:
            method for the new :class:`Request` object.
        :param url:
            URL for the new :class:`Request` object.
        :param name: (optional)
            Placeholder, make compatible with Locust's HttpSession
        :param params: (optional)
            Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional)
            Dictionary or bytes to send in the body of the :class:`Request`.
        :param headers: (optional)
            Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional)
            Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional)
            Dictionary of ``'filename': file-like-objects`` for multipart encoding upload.
        :param auth: (optional)
            Auth tuple or callable to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional)
            How long to wait for the server to send data before giving up, as a float, or \
            a (`connect timeout, read timeout <user/advanced.html#timeouts>`_) tuple.
            :type timeout: float or tuple
        :param allow_redirects: (optional)
            Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional)
            Dictionary mapping protocol to the URL of the proxy.
        :param stream: (optional)
            whether to immediately download the response content. Defaults to ``False``.
        :param verify: (optional)
            if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
        :param cert: (optional)
            if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        :param raw_mock_response: (optional)
            raw_mock_response for mock response prepare.
        """
        # create a new instance of SessionData for each request, to ensure data are isolated
        self.data = SessionData()

        # timeout default to 120 seconds
        kwargs.setdefault("timeout", 120)

        # set stream to True, in order to get client/server IP/Port
        kwargs["stream"] = True

        start_timestamp = time.time()

        # set header 'Date' to represent request timestamp
        now = datetime.now(timezone(timedelta(hours=8)))
        kwargs["headers"].update({"Date": now.strftime("%Y-%m-%d %H:%M:%S %Z")})

        requests_response = self._send_request_safe_mode(method, url, **kwargs)
        response_time_ms = round((time.time() - start_timestamp) * 1000, 2)

        # get length of the response content
        content_size = int(dict(requests_response.headers).get("Content-Length") or 0)

        # record the consumed time
        self.data.stat.response_time_ms = response_time_ms
        self.data.stat.elapsed_ms = requests_response.elapsed.microseconds / 1000.0
        self.data.stat.content_size = content_size

        # record request and response histories, include 30X redirection
        response_list = requests_response.history + [requests_response]

        # expand nested json if headers contain 'X-Json-Control' and its value is 'expand'
        is_expand_nested_json = False
        if kwargs["headers"].get("X-Json-Control") == "expand":
            is_expand_nested_json = True

        self.data.req_resps = [
            get_req_resp_record(
                requests_response_, is_expand_nested_json=is_expand_nested_json
            )
            for requests_response_ in response_list
        ]

        try:
            requests_response.raise_for_status()
        except RequestException as ex:
            logger.error(f"{str(ex)}")
        else:
            logger.info(
                f"status_code: {requests_response.status_code}, "
                f"response_time(ms): {response_time_ms} ms, "
                f"response_length: {content_size} bytes"
            )

        return requests_response

    def _send_request_safe_mode(self, method, url, **kwargs) -> Response:
        """
        Send a HTTP request, and catch any exception that might occur due to connection problems.
        Safe mode has been removed from requests 1.x.
        """
        # mock mode
        if raw_mock_response := kwargs.get("raw_mock_response", None):
            resp = MockResponse(**raw_mock_response)
            # keep request params,headers,data,json,cookies
            resp.request = Request(
                method,
                url,
                **get_sub_dict(
                    kwargs, *["params", "headers", "data", "json", "cookies"]
                ),
            ).prepare()
            return resp
        try:
            return requests.Session.request(self, method, url, **kwargs)
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except RequestException as ex:
            resp = ApiResponse()
            resp.error = ex
            resp.status_code = 0  # with this status_code, content returns None
            resp.request = (
                ex.request
                if hasattr(ex, "request") and ex.request
                else Request(method, url).prepare()
            )
            return resp
