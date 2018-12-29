# Functions for geoanalytics
# Author: D.Kisler <admin@dkisler.de>

import pandas as pd
import numpy as np
import requests
import time
import json
from shapely.geometry import (Point, #point
                              shape) # geopolygon


def routing(start, finish, apikey,
            mode,
            departure_ts=int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 09:00:00'), '%Y-%m-%d %H:%M:%S')))):
    """
    A2B Routing/Directions Google API
    https://developers.google.com/maps/documentation/directions

    Required:
    :param start: A address, or lat,lng pair
    :param finish: B address, or lat,lng pair
    :param apikey: API access keya
    :param mode: travaling mode [driving, walking, bicycling, transit]
    :param mode_transit: traffic transit mode
    Optional:
    :param departure_ts: - timestamp for public transport departure
    """

    from requests import get

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
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={finish}&mode=transit&transit_mode=rail|bus&departure_time={departure_ts}&key={apikey}'

    d = requests.get(url, headers={'accept': 'application/json'})

    if not d.ok:
        return {'distance': None, 'duration': None, 'details': None}

    d = d.json()
    return _routing_details(d)
