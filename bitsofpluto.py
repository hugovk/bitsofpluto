#!/usr/bin/env python
"""
Mastodon bot. Tooting a different bit of Pluto every six hours.
Photo by NASA's New Horizons spacecraft.
https://www.nasa.gov/image-feature/the-rich-color-variations-of-pluto/…
"""
from __future__ import annotations

import argparse
import os.path
import random
import sys
import tempfile
import webbrowser

import yaml  # pip install PyYAML
from mastodon import Mastodon  # pip install Mastodon.py
from PIL import Image  # pip install pillow

# No geolocation on Mastodon
# https://github.com/mastodon/mastodon/issues/8340
# import closest_point_to_pluto

WIDTHS = [600, 800, 1000, 1200, 2000]


def load_yaml(filename: str) -> dict[str, str]:
    """
    File should contain:
    mastodon_client_id: TODO_ENTER_YOURS
    mastodon_client_secret: TODO_ENTER_YOURS
    mastodon_access_token: TODO_ENTER_YOURS
    """
    with open(filename) as f:
        data = yaml.safe_load(f)

    if not data.keys() >= {
        "mastodon_client_id",
        "mastodon_client_secret",
        "mastodon_access_token",
    }:
        sys.exit(f"Mastodon credentials missing from YAML: {filename}")
    return data


def toot_it(
    status: str,
    credentials: dict[str, str],
    image_path: str = None,
    *,
    test: bool = False,
    no_web: bool = False,
) -> None:
    """Toot using credentials"""
    if len(status) <= 0:
        return

    # Create and authorise an app with (read and) write access following:
    # https://gist.github.com/aparrish/661fca5ce7b4882a8c6823db12d42d26
    # Store credentials in YAML file
    api = Mastodon(
        credentials["mastodon_client_id"],
        credentials["mastodon_client_secret"],
        credentials["mastodon_access_token"],
        api_base_url="https://botsin.space",
    )

    print("TOOTING THIS:\n", status)

    if test:
        print("(Test mode, not actually tooting)")
        return

    media_ids = []
    if image_path:
        print("Upload image")

        media = api.media_post(media_file=image_path)
        media_ids.append(media["id"])

    # No geolocation on Mastodon
    # https://github.com/mastodon/mastodon/issues/8340
    # lat, long = closest_point_to_pluto.closest_point_to_pluto()

    toot = api.status_post(status, media_ids=media_ids, visibility="public")

    url = toot["url"]
    print("Tooted:\n" + url)
    if not no_web:
        webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


def bitsofpluto(pluto_filename: str) -> str:
    """Get a bit of Pluto"""
    pluto = Image.open(pluto_filename)
    print(pluto.size)
    while True:
        width = random.choice(WIDTHS)
        height = width * 3 / 4
        print("width, height:", width, height)
        x = random.randrange(0, pluto.width - width + 1)
        y = random.randrange(0, pluto.height - height + 1)
        print("x, y: ", x, y)
        print("x + width, y + height: ", x + width, y + height)
        bit_of_pluto = pluto.crop((x, y, x + width, y + height))
        top = 0
        left = 0
        bottom = bit_of_pluto.height - 1
        right = bit_of_pluto.width - 1
        points = [
            (left, top),
            (right, top),
            (right / 2, top),
            (left, bottom / 2),
            (right, bottom / 2),
            (right / 2, bottom / 2),
            (left, bottom),
            (right, bottom),
            (right / 2, bottom),
        ]
        total_brightness = 0
        total_dark_points = 0
        for point in points:
            r, g, b = bit_of_pluto.getpixel(point)
            brightness = sum([r, g, b]) / 3  # 0 is black and 255 is white
            print("r, g, b, brightness: ", r, g, b, brightness)
            total_brightness += brightness
            if brightness < 10:
                total_dark_points += 1

        print("total_brightness: ", total_brightness)
        print("total_dark_points: ", total_dark_points)

        if total_dark_points <= 6:
            # bit_of_pluto.show()
            break
    outfile = os.path.join(tempfile.gettempdir(), "bitofpluto.jpg")
    print("outfile: " + outfile)
    bit_of_pluto.save(outfile, quality=95)
    return outfile


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tooting a different bit of Pluto every six hours.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-y",
        "--yaml",
        default="M:/bin/data/bitsofpluto.yaml",
        help="YAML file location containing Mastodon keys and secrets",
    )
    parser.add_argument(
        "-nw",
        "--no-web",
        action="store_true",
        help="Don't open a web browser to show the tooted toot",
    )
    parser.add_argument(
        "-x",
        "--test",
        action="store_true",
        help="Test mode: go through the motions but don't toot anything",
    )
    parser.add_argument(
        "-p",
        "--pluto",
        default="data/crop_p_color2_enhanced_release.7000x7000.png",
        help="Path to a big photo of Pluto",
    )
    args = parser.parse_args()

    credentials = load_yaml(args.yaml)

    image_path = bitsofpluto(args.pluto)

    status = "A bit of Pluto"

    toot_it(status, credentials, image_path, test=args.test, no_web=args.no_web)


if __name__ == "__main__":
    main()
