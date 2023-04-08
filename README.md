spotimoo
========

[![Tests Status][TestStatusImageLink]][TestStatusLink] [![Documentation Status][DocsStatusLink]][DocsStatusImageLink]

Tiny library that provides access to the [Spotify Web API][SpotifyWebAPI].

Documentation
-------------

Spotimoo's full documentation is online at [Spotimoo Documentation][SpotimooDocumentation].

Installation
------------

```sh
python3 -m pip install "git+https://github.com/spotimoo/spotimoo.git"
```

Quick Start
-----------

```python
from spotimoo import Spotimoo


spotimoo = Spotimoo(client_id="CLIENT_ID_TOKEN",
                    client_secret="CLIENT_SECRET_TOKEN")
    
track_id = "4cOdK2wGLETKBW3PvgPWqT"
result = spotimoo.track(track_id).json()

print(result["artists"][0]["name"])     # Rick Astley
print(result["name"])                   # Never Gonna Give You Up
```

License
-------

Spotimoo is made available under the terms of either the MIT License. See the
[LICENSE][License] files for license details.

[TestStatusImageLink]: https://github.com/spotimoo/spotimoo/actions/workflows/tests.yml/badge.svg
[TestStatusLink]: https://github.com/spotimoo/spotimoo/actions/workflows/tests.yml
[DocsStatusLink]: https://readthedocs.org/projects/spotimoo/badge/?version=latest
[DocsStatusImageLink]: https://spotimoo.readthedocs.io/en/latest/?badge=latest
[SpotifyWebAPI]: https://developer.spotify.com/documentation/web-api
[SpotimooDocumentation]: https://spotimoo.readthedocs.io/en/latest/
[License]: ./LICENSE
