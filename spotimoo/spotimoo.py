from typing import Callable, Self
from base64 import b64encode
from functools import wraps

from requests import request
from requests.models import Response
from six import text_type

from .exceptions import IncorrectRequest


def _validate_request(function: Callable) -> Callable:
    """Check if the request was processed correctly.

    :param function: Decorated function that returns a response
    :type: typing.Callable
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        if not response.ok:
            raise IncorrectRequest(response.status_code)
        return response

    return wrapper


class Spotimoo:
    """Spotimoo is a base class that provides an interface to the Spotify API.

    :param client_id: Client ID field from Spotify API that must be supplied or
        set as enviroment variable
    :type client_id: str
    :param client_secret: Client Secret field from Spotify API that must be
        supplied or set as enviroment variable
    :type client_secret: str
    :param timeout: How long will you have to wait to get a message about a
        failed request
    :type timeout: int, optional
    """

    def __init__(
        self: Self, client_id: str, client_secret: str, *, timeout: int = 10
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self.token = self._generate_token()

    def __str__(self: Self) -> str:
        return (
            f"Spotimoo(client_id={self.client_id}, "
            f"client_secret={self.client_secret}, timeout={self.timeout})"
        )

    def __repr__(self: Self) -> str:
        return (
            f"Spotimoo(client_id={self.client_id}, "
            f"client_secret={self.client_secret}, timeout={self.timeout})"
        )

    @_validate_request
    def _generate_token_response(self: Self) -> Response:
        """Request to Spotify API that provides user OAuth access token creation.

        :return: Response to this request
        :rtype: requests.model.Response
        """
        data = {"grant_type": "client_credentials"}

        authorization = b64encode(
            text_type(self.client_id + ":" + self.client_secret).encode("ascii")
        )
        headers = {"Authorization": f"Basic {authorization.decode('ascii')}"}

        return request(
            "POST",
            "https://accounts.spotify.com/api/token",
            data=data,
            headers=headers,
            verify=True,
            timeout=self.timeout,
        )

    def _generate_token(self: Self) -> str:
        """Give user completely new generated access token for future requests.

        This token will be valid for 1 hour, then it will need to renewed.

        :return: OAuth access token to Spotify API
        :rtype: str
        """
        response = self._generate_token_response().json()
        return response["access_token"]

    @_validate_request
    def track(self: Self, track_id: str) -> Response:
        """Request that return response with track information.

        :param track_id: Track identifier in Spotify. For example:

            Link: https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT?si=5e9a14dc868948da

            Track ID: 4cOdK2wGLETKBW3PvgPWqT
        :type track_id: str
        :return: Response to this request
        :rtype: requests.model.Response
        """
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
