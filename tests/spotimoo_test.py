from os import getenv
from unittest.mock import patch
from io import StringIO

from pytest import raises

from spotimoo.spotimoo import Spotimoo
from spotimoo.exceptions import IncorrectRequest


def test_str_dunder_method(client_id, client_secret, spotimoo) -> None:
    actual = str(spotimoo)
    expect = (
        f"Spotimoo(client_id={client_id}, client_secret={client_secret}, timeout=10)"
    )

    assert expect == actual


def test_repr_dunder_method(client_id, client_secret, spotimoo) -> None:
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        print(spotimoo)

    actual = mock_stdout.getvalue()
    expect = (
        f"Spotimoo(client_id={client_id}, client_secret={client_secret}, timeout=10)\n"
    )

    assert expect == actual

    actual = spotimoo.__repr__()
    expect = (
        f"Spotimoo(client_id={client_id}, client_secret={client_secret}, timeout=10)"
    )

    assert expect == actual


def test_incorrect_request(spotimoo) -> None:
    track_id = "invalid_track_id"
    with raises(IncorrectRequest) as exception:
        spotimoo.track(track_id)

    assert exception.value.status_code == 400


def test_correct_track(spotimoo) -> None:
    track_id = "4cOdK2wGLETKBW3PvgPWqT"
    result = spotimoo.track(track_id).json()

    actual = result["artists"][0]["name"]
    expect = "Rick Astley"

    assert expect == actual

    actual = result["name"]
    expect = "Never Gonna Give You Up"

    assert expect == actual


def test_correct_album(spotimoo) -> None:
    album_id = "0XRZpF083HqgygM0v1hQyE"
    result = spotimoo.album(album_id).json()

    actual = result["artists"][0]["name"]
    expect = "The Beatles"

    assert expect == actual

    actual = result["name"]
    expect = "Yellow Submarine Songtrack"

    assert expect == actual


def test_correct_artist(spotimoo) -> None:
    artist_id = "4NJhFmfw43RLBLjQvxDuRS"
    result = spotimoo.artist(artist_id).json()

    actual = result["name"]
    expect = "Wolfgang Amadeus Mozart"

    assert expect == actual


def test_correct_user(spotimoo) -> None:
    user_id = "216ndgqqr2hlj3be4gf3rjzoa"
    result = spotimoo.user(user_id).json()

    actual = result["type"]
    expect = "user"

    assert expect == actual


def test_correct_playlist(spotimoo) -> None:
    playlist_id = "3sWRnit5VevDAQGiBoPpmP"
    result = spotimoo.playlist(playlist_id).json()

    actual = result["owner"]["display_name"]
    expect = "Egor Bronnikov"

    assert expect == actual
