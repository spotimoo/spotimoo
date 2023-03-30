__all__ = ["Spotimoo"]

from typing import Callable, Self
from base64 import b64encode
from functools import wraps, reduce
from urllib.parse import urljoin

from requests import request
from requests.models import Response
from six import text_type

from .exceptions import IncorrectRequest


def _validate_request(function: Callable) -> Callable:
    """Check if the request was processed correctly.

    :param function: Decorated function that returns a response
    :type function: typing.Callable
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        if not response.ok:
            raise IncorrectRequest(response.status_code)
        return response

    return wrapper


def _build_url(*urls: str) -> str:
    """Build a URL address from sequence of parts.

    :param urls: Sequence of URL parts
    :type urls: str
    :return: URL address
    :rtype: str
    """
    return reduce(urljoin, urls)


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
    def _spotify_get(
        self: Self, request_: str, id_: str, *, options: str = ""
    ) -> Response:
        """Represent basic pattern for GET request Spotify API.

        :param request_: Main request URL
        :type request_: str
        :param id_: Request identifier
        :type id_: str
        :param options: Query options for request
        :type options: str, optional
        """
        headers = {
            "Accept": "applications/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        return request(
            "GET",
            _build_url(request_, id_, options),
            headers=headers,
            timeout=self.timeout,
        )

    def track(self: Self, track_id: str) -> Response:
        """Request that return response with track information.

        :param track_id: Track identifier in Spotify. For example:

            Link: https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT?si=5e9a14dc868948da

            Track ID: 4cOdK2wGLETKBW3PvgPWqT
        :type track_id: str
        :return: Response to this request
        :rtype: requests.model.Response
        """
        return self._spotify_get("https://api.spotify.com/v1/tracks/", track_id)

    def album(self: Self, album_id: str) -> Response:
        """Request that return response with album information.

        :param album_id: Album identifier in Spotify. For example:

            Link: https://open.spotify.com/album/0XRZpF083HqgygM0v1hQyE?si=fnZU07tQSYuWJrve5LgTOQ

            Album ID: 0XRZpF083HqgygM0v1hQyE
        :type album_id: str
        :return: Response to this request
        :rtype: requests.model.Response
        """
        return self._spotify_get("https://api.spotify.com/v1/albums/", album_id)

    def artist(self: Self, artist_id: str) -> Response:
        """Request that return response with artist information.

        :param artist_id: Artist identifier in Spotify. For example:

            Link: https://open.spotify.com/artist/4NJhFmfw43RLBLjQvxDuRS?si=RsXekpUYRsWO1t_-oxs2Ew

            Artist ID: 4NJhFmfw43RLBLjQvxDuRS
        :type artist_id: str
        :return: Response to this request
        :rtype: requests.model.Response
        """
        return self._spotify_get("https://api.spotify.com/v1/artists/", artist_id)

    def user(self: Self, user_id: str) -> Response:
        """Request that return response with user information.

        :param user_id: User identifier in Spotify. For example:

            Link: https://open.spotify.com/user/216ndgqqr2hlj3be4gf3rjzoa?si=defb0c8c29204b09

            User ID: 216ndgqqr2hlj3be4gf3rjzoa
        :type user_id: str
        :return: Response to this request
        :rtype: requests.model.Response
        """
        return self._spotify_get("https://api.spotify.com/v1/users/", user_id)

    def playlist(self: Self, playlist_id: str) -> Response:
        """Request that return response with playlist information.

        :param playlist_id: Playlist identifier in Spotify. For example:

            Link: https://open.spotify.com/playlist/3sWRnit5VevDAQGiBoPpmP?si=781fc19fd6674f60

            Playlist ID: 3sWRnit5VevDAQGiBoPpmP
        :type playlist_id: str
        :return: Response to this request
        :rtype: requests.model.Response
        """
        return self._spotify_get(
            "https://api.spotify.com/v1/playlists/",
            playlist_id,
            options="?fields=name%2Cimages%2Cowner",
        )
