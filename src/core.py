import urllib3
from session import HTTPSessionManager


class Request:
    def __init__(self, method):
        self.method = method
        self.session_manager = HTTPSessionManager()

    def request(self, url: str, headers=None, body=None):
        """
        Send an HTTP request using the specified method.

        :param method: HTTP method (GET, POST, etc.)
        :param url: URL for the request
        :param headers: Optional dictionary of headers
        :param body: Optional body for the request (used in POST, PUT, etc.)
        :return: urllib3.response.HTTPResponse object
        """


        match self.method.upper():
            case "POST":
                return self.session_manager.request(
                    method="POST", url=url, headers=headers, body=body
                )
            case "GET":
                return self.session_manager.request(
                    method="GET", url=url, headers=headers
                )
            case "PUT":
                return self.session_manager.request(
                    method="PUT", url=url, headers=headers, body=body
                )
            case "DELETE":
                return self.session_manager.request(
                    method="DELETE", url=url, headers=headers
                )
            case _:
                return self.session_manager.request(
                    method="GET", url=url, headers=headers
                )
    