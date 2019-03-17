# Functions for geoanalytics
# Author: D.Kisler <admin@dkisler.de>

import pandas as pd
import numpy as np
import requests
import time
import json
from shapely.geometry import (Point,  # point
                              shape)  # geopolygon


def routing_here(start, finish,
                 app_id, app_code,
                 mode,
                 departure_ts='now',
                 walk_speed=None,
                 walk_radius=None,
                 max_number_of_changes=None,
                 alternatives=None):
    """
    Function to fetch data via HERE maps routing API

    Pedestrian+public transport routing from A to B
    Details: https://developer.here.com/documentation/routing/topics/request-public-transport-routes.html

    :param start: lat,lng pair of the point A, e.g. 52.530,13.326
    :param finish: lat,lng pair of the point B, e.g. 52.513,13.407
    :param app_id: HERE maps app ID
    :param app_code: HERE maps app code
    :param mode: routing mode

    Optional:
    :param departure_ts: - timestamp for public transport departure
    :param walk_speed: speed of walk im meters per sec.
    :param walk_radius: max walking radius to A and from B. from 0 to 6000 meters
    :param max_number_of_changes: for public transport
    :param alternatives: alternatives for A-to-B connections. 0 - best route returend, max number is 3
    """

    URL = "https://route.api.here.com/routing/7.2/calculateroute.json"

    URL_params = {
        "waypoint0": start,
        "waypoint1": finish,
        "app_id": app_id,
        "app_code": app_code,
        "mode": mode,
        "departure": departure_ts
        }

    if walk_speed:
        URL_params['walkSpeed'] = walk_speed
    if alternatives:
        URL_params['alternatives'] = alternatives
    if walk_radius:
        URL_params['walkRadius'] = walk_radius
    if max_number_of_changes:
        URL_params['maxNumberOfChanges'] = max_number_of_changes

    try:
        d = requests.get(url=URL, params=URL_params)

        if d.ok:
            return d.json(), None
        else:
            return None, f"API status code: {d.status_code}"

    except Exception as ex:
        return None, ex


def routing_google(start, finish,
                   apikey,
                   mode, mode_transit=None,
                   departure_ts=int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 09:00:00'), '%Y-%m-%d %H:%M:%S')))):
    """
    A2B Routing/Directions Google API
    https://developers.google.com/maps/documentation/directions

    Required:
    :param start: A address, or lat,lng pair
    :param finish: B address, or lat,lng pair
    :param apikey: API access key
    :param mode: travaling mode [driving, walking, bicycling, transit]
    :param mode_transit: traffic transit mode
    Optional:
    :param departure_ts: - timestamp for public transport departure
    """

    def _routing_details(d):
        """Routes details"""
        routes = []

        for route in range(len(d['routes'])):

            route = d['routes'][route]['legs'][0]

            r = {k: route[k]['value'] for k in ['duration', 'distance']}
            r['details'] = {}

            for step in route['steps']:
                mode = step['travel_mode']

                if mode not in r['details'].keys():
                    r['details'][mode] = {k: step[k]['value']
                                          for k in ['duration', 'distance']}
                    r['details'][mode]['n_change'] = 0
                else:
                    r['details'][mode]['distance'] += step['distance']['value']
                    r['details'][mode]['duration'] += step['duration']['value']
                    r['details'][mode]['n_change'] += 1
            routes.append(r)

        return routes

    start = start.replace(' ', '+')
    finish = finish.replace(' ', '+')
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={finish}&mode={mode}&departure_time={departure_ts}&key={apikey}'

    if mode_transit:
        url += f'&transit_mode={mode_transit}'

    d = requests.get(url, headers={'accept': 'application/json'})

    if not d.ok:
        return {'distance': None, 'duration': None, 'details': None}

    d = d.json()
    return _routing_details(d)


def dist_geo_np(lat_start, lon_start,
                lat_stop, lon_stop,
                unit='m'):
    """
    Geodesic distance between two points

    :param lat_start, lon_start: lat, lon of the starting point
    :param lat_stop, lon_stop: lat, lon of the end point
    :param unit: distance unit [m, km]
    """

    lat_coef = 110574
    lon_coef = 111320

    if unit == 'km':
        lat_coef = lat_coef / 1000.
        lon_coef = lon_coef / 1000.

    try:

        dist = np.sqrt(
            np.power(np.multiply(lon_start, np.multiply(lon_coef, np.cos(np.multiply(lat_start, np.pi / 180))))
                     - np.multiply(lon_stop, np.multiply(lon_coef, np.cos(np.multiply(lat_stop, np.pi / 180)))), 2)
            + np.power(np.multiply(lat_start, lat_coef) -
                       np.multiply(lat_stop, lat_coef), 2))

        return dist, None

    except Exception as ex:

        return None, ex


def dist_geo(lat_start, lon_start,
             lat_stop, lon_stop,
             unit='m'):
    """
    Geodesic distance between two points

    :param lat_start, lon_start: lat, lon of the starting point
    :param lat_stop, lon_stop: lat, lon of the end point
    :param unit: distance unit [m, km]
    """

    lat_coef = 110574
    lon_coef = 111320

    if unit == 'km':
        lat_coef = lat_coef / 1000.
        lon_coef = lon_coef / 1000.

    return np.sqrt(np.power(lon_start * lon_coef * np.cos(lat_start * np.pi / 180)
                            - lon_stop * lon_coef * np.cos(lat_stop * np.pi / 180), 2) +
                   np.power(lat_start * lat_coef - lat_stop * lat_coef, 2))
