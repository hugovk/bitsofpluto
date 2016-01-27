#!/usr/bin/env python
# encoding: utf-8
"""
Find the point on Earth closest to Pluto right now.

Or thereabouts.

http://astronomy.stackexchange.com/a/13318/4166
"""
from __future__ import print_function
import ephem
import webbrowser

NINETY = ephem.degrees(90)


def closest_point_to_pluto():

    pluto = ephem.Pluto()
    obs = ephem.Observer()
    now = ephem.now()

    # http://stackoverflow.com/a/477610/724176
    def drange(start, stop, step):
        """Decimal range"""
        r = start
        while r < stop:
            yield r
            r += step

    def calc_best(min_lat=-90, max_lat=90,
                  min_lon=-180, max_lon=180,
                  step=10):
        """Check a bunch of lat/lon points and find the one where
        Pluto's observed altitude is closest to 90 degrees"""
        best_alt = 0
        best_az = None
        best_lat = None
        best_lon = None

        for lat in drange(min_lat, max_lat+1, step):
            for lon in drange(min_lon, max_lon+1, step):
                obs.lon = str(lon)
                obs.lat = str(lat)
                obs.date = now
                pluto.compute(obs)

                if abs(pluto.alt - NINETY) < abs(best_alt - NINETY):
                    best_alt = pluto.alt
                    best_az = pluto.az
                    best_lat = lat
                    best_lon = lon
                    # print(lat, lon, pluto.alt, pluto.az)

        print("Best:")
        print(best_lat, best_lon, best_alt, best_az)
        return best_lat, best_lon

    best_lat, best_lon = calc_best()
    last_step = 10
    for step in [1, 0.1, 0.01]:
        best_lat, best_lon = calc_best(best_lat-last_step, best_lat+last_step,
                                       best_lon-last_step, best_lon+last_step,
                                       step)
        last_step = step

    return best_lat, best_lon

if __name__ == "__main__":
    lat, lon = closest_point_to_pluto()

    osm = "https://www.openstreetmap.org/?mlat={0}&mlon={1}#map=3/{0}/{1}"
    url = osm.format(lat, lon)
    print(url)
    webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible

# End of file
