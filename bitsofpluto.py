#!/usr/bin/env python
"""
Twitter bot. Tweeting a different bit of Pluto every six hours.
Photo by NASA's New Horizons spacecraft.
https://www.nasa.gov/image-feature/the-rich-color-variations-of-pluto/…
"""

import argparse
import os.path
import random
import sys
import tempfile
import webbrowser

import twitter  # pip install twitter
import yaml  # pip install PyYAML

import closest_point_to_pluto
from PIL import Image  # pip install pillow

WIDTHS = [600, 800, 1000, 1200, 2000]


def load_yaml(filename):
    """
    File should contain:
    consumer_key: TODO_ENTER_YOURS
    consumer_secret: TODO_ENTER_YOURS
    access_token: TODO_ENTER_YOURS
    access_token_secret: TODO_ENTER_YOURS
    """
    with open(filename) as f:
        data = yaml.safe_load(f)

    keys = data.viewkeys() if sys.version_info.major == 2 else data.keys()
    if not keys >= {
        "access_token",
        "access_token_secret",
        "consumer_key",
        "consumer_secret",
    }:
        sys.exit("Twitter credentials missing from YAML: " + filename)
    return data


def tweet_it(string, credentials, image=None):
    """ Tweet string using credentials """
    if len(string) <= 0:
        return

    # Create and authorise an app with (read and) write access at:
    # https://dev.twitter.com/apps/new
    # Store credentials in YAML file
    auth = twitter.OAuth(
        credentials["access_token"],
        credentials["access_token_secret"],
        credentials["consumer_key"],
        credentials["consumer_secret"],
    )
    t = twitter.Twitter(auth=auth)

    print("TWEETING THIS:\n", string)

    if args.test:
        print("(Test mode, not actually tweeting)")
    else:

        if image:
            print("Upload image")

            # Send images along with your tweets.
            # First just read images from the web or from files the regular way
            with open(image, "rb") as imagefile:
                imagedata = imagefile.read()
            t_up = twitter.Twitter(domain="upload.twitter.com", auth=auth)
            id_img = t_up.media.upload(media=imagedata)["media_id_string"]
        else:
            id_img = None  # Does t.statuses.update work with this?

        lat, long = closest_point_to_pluto.closest_point_to_pluto()
        result = t.statuses.update(
            status=string,
            media_ids=id_img,
            lat=lat,
            long=long,
            display_coordinates=True,
        )

        url = (
            "http://twitter.com/"
            + result["user"]["screen_name"]
            + "/status/"
            + result["id_str"]
        )
        print("Tweeted:\n" + url)
        if not args.no_web:
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


def bitsofpluto(pluto_filename):
    """ Get a bit of Pluto """
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tweeting a different bit of Pluto every six hours.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-y",
        "--yaml",
        default="M:/bin/data/bitsofpluto.yaml",
        help="YAML file location containing Twitter keys and secrets",
    )
    parser.add_argument(
        "-nw",
        "--no-web",
        action="store_true",
        help="Don't open a web browser to show the tweeted tweet",
    )
    parser.add_argument(
        "-x",
        "--test",
        action="store_true",
        help="Test mode: go through the motions but don't tweet anything",
    )
    parser.add_argument(
        "-p",
        "--pluto",
        default="M:/bin/data/pluto/crop_p_color2_enhanced_release.7000x7000.png",
        help="Path to a big photo of Pluto",
    )
    args = parser.parse_args()

    credentials = load_yaml(args.yaml)

    image = bitsofpluto(args.pluto)

    tweet = "A bit of Pluto"

    tweet_it(tweet, credentials, image)

# End of file
