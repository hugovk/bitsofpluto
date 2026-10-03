# [@bitsofpluto](https://mas.to/@bitsofpluto)

[![Test](https://github.com/hugovk/bitsofpluto/actions/workflows/test.yml/badge.svg)](https://github.com/hugovk/bitsofpluto/actions/workflows/test.yml)
[![Python: 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)

Mastodonbot. Toots a different bit of Pluto every six hours.

See the Mastodon bot in action at
**[![](https://mas.to/favicon.ico)@bitsofpluto](https://mas.to/@bitsofpluto)**.

## How it runs

[`toot.yml`](.github/workflows/toot.yml) runs on GitHub Actions every six hours. The
Mastodon credentials YAML is stored in the `BITSOFPLUTO_YAML` repository secret. To run
it by hand, or for a dry run that doesn't toot, use "Run workflow" on the
[Actions tab](https://github.com/hugovk/bitsofpluto/actions/workflows/toot.yml).
