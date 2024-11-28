import urllib3
from urllib3.util.retry import Retry
from .exceptions import HTTPRequestException


class HTTPSessionManager:
    """
    Centralized session manager for HTTP requests with retry policy.
    """

    def __init__(self, retries=3, backoff_factor=0.3):
        self.http = urllib3.PoolManager()
        self.retries = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )

    def request(self, method, url, headers=None, body=None):
        """
        Make an HTTP request using the managed session.

        :param method: HTTP method (GET, POST, etc.)
        :param url: URL for the request
        :param headers: Optional headers dictionary
        :param body: Optional request body
        :return: urllib3.response.HTTPResponse object
        """
        response = self.http.request(
            method=method,
            url=url,
            headers=headers,
            body=body,
            retries=self.retries,
        )
        return response