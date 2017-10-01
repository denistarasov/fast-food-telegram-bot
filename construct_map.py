import json
import logging
import os
import requests

# geocoding_api_token = os.environ[""]
geocoding_api_token = ''
places_api_token = ''
geocoding_url = 'https://maps.googleapis.com/maps/api/geocode/json'
static_map_url = 'https://maps.googleapis.com/maps/api/staticmap'
nearby_search_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'


def address_to_geopoint(address):
    params = {
        'address': address,
        'key': geocoding_api_token
    }
    response = requests.get(url=geocoding_url, params=params)
    parsed_json = json.loads(response.text)
    # print(response.status_code)
    # print(type(parsed_json))
    geopoint = parsed_json['results'][0]['geometry']['location']
    print('geopoint: {}'.format(geopoint))
    return geopoint


def find_restaurants_nearby(geopoint, keyword):
    '?location=-33.8670522,151.1957362&radius=500&type=restaurant&keyword=cruise&key=YOUR_API_KEY'
    params = {
        'location': str(geopoint['lat']) + ',' + str(geopoint['lng']),
        'keyword': keyword,
        # 'rankby': 'distance',
        'type': 'restaurant',
        'key': places_api_token,
        'radius': 1500 # not allowed if rankby=distance specified
    }
    response = requests.get(url=nearby_search_url, params=params)
    parsed_json = json.loads(response.text)
    restaurants_geopoints = []
    for restaurant in parsed_json['results']:
        restaurant_geopoint = restaurant['geometry']['location']
        print(restaurant_geopoint)
        restaurants_geopoints.append(restaurant_geopoint)
    return restaurants_geopoints


def geopoints_to_markers(geopoints):
    markers = []
    for key in geopoints.keys():
        s = 'color:' + key
        for point in geopoints[key]:
            s += '|{},{}'.format(point['lat'], point['lng'])
        markers.append(s)
    return markers


def restaurants_to_map(markers):
    params = {
        # 'center': 'Russia,Moscow',
        # 'zoom': '13',
        'size': '600x300',
        'maptype': 'roadmap',
        'markers': markers,
        'key': geocoding_api_token
    }
    r = requests.Request('GET', static_map_url, params=params).prepare()
    return r.url


def construct_map(address='красная площадь'):
    address = address.encode('utf-8')
    logging.info("Constructing map for address: {}".format(address))
    central_point = address_to_geopoint(address)
    geopoints = {
        'yellow': find_restaurants_nearby(central_point, 'mcdonalds|макдональдс'),
        'black': find_restaurants_nearby(central_point, 'kfc'),
        'red': find_restaurants_nearby(central_point, 'burger king')
    }
    markers = geopoints_to_markers(geopoints)
    restaurants_map_url = restaurants_to_map(markers)
    logging.info("Sent map: {}".format(restaurants_map_url))
    return restaurants_map_url


if __name__ == '__main__':
    print(construct_map())
