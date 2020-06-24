import json

import requests
from redis import Redis
from flask import render_template, request, jsonify

from views import bp


cache = Redis(host="redis")


# define hello world page
@bp.route('/')
def hello_world():
    return 'Hello, World!'


@bp.route('/stores')
def stores():

    with open("/tmp/stores.json") as json_data:
        stores = json.load(json_data)

    stores.sort(key=lambda store: store['name'])

    for store in stores:

        # If available use cache to reduce API queries.
        if coordinates := cache.get(store['postcode']):
            store['coordinates'] = coordinates.decode('utf-8')
            continue

        response = requests.get(f"http://api.postcodes.io/postcodes/{store['postcode']}")
        if response.ok:
            postcode_data = response.json()
            result = postcode_data["result"]
            store['coordinates'] = f"{result['latitude']}, {result['longitude']}"
        else:
            store['coordinates'] = "N/A"

        # If we had to query the external API, save it in cache for future usage.
        cache.set(store['postcode'], store['coordinates'].encode('utf-8'))

    return render_template('stores.html', title='Stores', stores=stores)


@bp.route('/stores_plus')
def stores_plus():

    # If available use cache to reduce API queries.
    if not stores := cache.get('stores'):

        with open("/tmp/stores.json") as json_data:
            stores = json.load(json_data)

        stores.sort(key=lambda store: store['name'])

        postcode_list = [store['postcode'] for store  in stores]

        payload = {"postcodes": postcode_list}
    
        response = requests.post("http://api.postcodes.io/postcodes/", json=payload)

        response_data = response.json()

        results = response_data['result']

        for store in stores:
            for result in results:
                if result["query"] == store["postcode"]:
                    if result['result'] is None:
                        continue

                    result = result['result']
                    store['coordinates'] = f"{result['latitude']}, {result['longitude']}"

        cache.set('stores', stores)


    return render_template('stores.html', title='Stores', stores=stores)



@bp.route('/find', methods=['POST'])
def finder():
    """ Searches for a store within a given postcode radius.

        Limitations: Maximum of 100 postcodes returned, maximum radius of 2km.

        Example request:
        curl http://localhost/find -d '{"radius": 2000, "postcode": "CT1 1DS"}' -H 'Content-Type: application/json'
    """

    post_data = request.get_json()

    # First, let's retrieve the coordinates for the postcode given
    response = requests.get(f"http://api.postcodes.io/postcodes/{post_data['postcode']}")

    response_data = response.json()

    latitude = response_data['result']['latitude']
    longitude = response_data['result']['longitude']

    # Now, let's request all postcodes within the radius of the coordinates
    post_parameters = {
        "geolocations": [{
        "longitude": longitude,
        "latitude": latitude,
        "radius": post_data['radius'],
        "limit": 100
        }]
    }

    response = requests.post(f"http://api.postcodes.io/postcodes/", json=post_parameters)

    response_data = response.json()

    raw_entries = response_data['result'][0]['result']
    postcodes = [entry['postcode'] for entry in raw_entries]

    # Next, check if any of the postcodes returned matches a store.
    with open("/tmp/stores.json") as json_data:
        stores = json.load(json_data)

    stores_within_radius = []

    for store in stores:
        if store['postcode'] in postcodes:
            stores_within_radius.append(store)

    return jsonify(stores=stores_within_radius)
