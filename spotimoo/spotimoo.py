from typing import Callable
from base64 import b64encode

from requests import request
from requests.models import Response
from six import text_type

from .exceptions import IncorrectRequest


def _validate_request(function: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        if not response.ok:
            raise IncorrectRequest(response.status_code)
        return response

    return wrapper


class Spotimoo:
    def __init__(
        self, client_id: str, client_secret: str, *, timeout: int = 10
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self.token = self._generate_token()

    def __str__(self):
        return (
            f"Spotimoo(client_id={self.client_id}, "
            f"client_secret={self.client_secret}, timeout={self.timeout})"
        )

    def __repr__(self):
        return (
            f"Spotimoo(client_id={self.client_id}, "
            f"client_secret={self.client_secret}, timeout={self.timeout})"
        )

    @_validate_request
    def _generate_token_response(self) -> Response:
        data = {"grant_type": "client_credentials"}

        authortization = b64encode(
            text_type(self.client_id + ":" + self.client_secret).encode("ascii")
        )
        headers = {"Authorization": f"Basic {authortization.decode('ascii')}"}

        return request(
            "POST",
            "https://accounts.spotify.com/api/token",
            data=data,
            headers=headers,
            verify=True,
            timeout=self.timeout,
        )

    def _generate_token(self) -> str:
        response = self._generate_token_response().json()
        return response["access_token"]

    @_validate_request
    def track(self, track_id: str) -> Response:
        headers = {
            "Accept": "applications/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        return request(
            "GET",
            f"https://api.spotify.com/v1/tracks/{track_id}",
            headers=headers,
            timeout=self.timeout,
        )
