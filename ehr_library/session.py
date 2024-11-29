import urllib3
from urllib3.util.retry import Retry


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

    def request(self, method, url, headers=None, body=None, download_path=None):
        """
        Make an HTTP request using the managed session.

        :param method: HTTP method (GET, POST, etc.)
        :param url: URL for the request
        :param headers: Optional headers dictionary
        :param body: Optional request body
        :param download_path: Optional path to save the response content as a file.
        :return: Response data or path to the saved file.
        """
        response = self.http.request(
            method=method,
            url=url,
            headers=headers,
            body=body,
            retries=self.retries,
        )

        if download_path and method.upper() == "GET" and response.status == 200:
            try:
                with open(download_path, "wb") as file:
                    file.write(response.data)
                return {"message": "File downloaded successfully", "path": download_path}
            except IOError as e:
                return {"error": f"Failed to save file: {e}"}
        else:
            return {
                "status": response.status,
                "data": response.data.decode('utf-8') if response.data else None,
            }