import urllib3
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from http.cookiejar import CookieJar
from .session import HTTPSessionManager
from .sockets import WebSocketManager


class Request:
    def __init__(self, method, debug=False):
        self.method = method
        self.session_manager = HTTPSessionManager()
        self.debug = debug

    def _sanitize_headers(self, headers):
        if not headers:
            return {}

        sanitized = headers.copy()
        sensitive_keys = {"Authorization", "Cookie", "Set-Cookie"}
        for key in sensitive_keys:
            sanitized[key] = "[REDACTED]"

        return sanitized

    def _log_request(self, method, url, headers, params=None):
        if self.debug:
            sanitized_headers = self._sanitize_headers(headers)
            print("DEBUG: HTTP Request")
            print(f'Method::: {method}')
            print(f'Url::: {url}')
            if params:
                print(f'Params::: {params}')
            print(f'Headers::: {sanitized_headers}')

    def build_url(self, base_url, params=None):
        """
        Constrói uma URL com query strings adicionadas ou atualizadas.

        :param base_url: URL base.
        :param params: Dicionário contendo os parâmetros de consulta.
        :return: URL com query strings.
        """
        if not params:
            return base_url

        # Parseia a URL existente
        parsed_url = urlparse(base_url)
        existing_params = parse_qs(parsed_url.query)

        # Atualiza os parâmetros existentes com os novos
        existing_params.update(params)

        # Reconstrói a URL com os novos parâmetros
        new_query_string = urlencode(existing_params, doseq=True)
        new_url = urlunparse((
            parsed_url.scheme, parsed_url.netloc, parsed_url.path,
            parsed_url.params, new_query_string, parsed_url.fragment
        ))

        return new_url

    def request(self, url: str, headers=None, body=None, params=None):
        """
        Send an HTTP request using the specified method.

        :param method: HTTP method (GET, POST, etc.)
        :param url: URL for the request
        :param headers: Optional dictionary of headers
        :param body: Optional body for the request (used in POST, PUT, etc.)
        :return: urllib3.response.HTTPResponse object
        """

        url = self.build_url(url, params)
        self._log_request(self.method, url, headers, params)

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
