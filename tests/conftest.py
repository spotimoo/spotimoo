from spotimoo.spotimoo import Spotimoo
from os import getenv

from pytest import fixture


def environment_variable(name: str) -> str:
    client_id = getenv(name)
    if not client_id:
        assert False
    return client_id


@fixture
def client_id() -> str:
    return environment_variable("CLIENT_ID")


@fixture
def client_secret() -> str:
    return environment_variable("CLIENT_SECRET")


@fixture
def spotimoo(client_id, client_secret) -> Spotimoo:
    return Spotimoo(client_id, client_secret)


@fixture
def token(spotimoo) -> str:
    return spotimoo.token
