import os
import requests

class GeocodingClient:
    def __init__(self, api_key=None, request_id=None):
        self.api_key = api_key or os.getenv("ola_api_key")
        self.request_id = request_id or os.getenv("ola_requestor_id")
        self.base_url = 'https://api.olamaps.io/places/v1'
        self.headers = {
            'X-Request-Id': self.request_id
        }
        if not self.api_key or not self.request_id:
            raise ValueError("API key and Request ID must be provided")

    def _make_request(self, endpoint, params):
        url = f'{self.base_url}/{endpoint}'
        params['api_key'] = self.api_key
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def reverse_geocode(self, latitude, longitude):
        params = {
            'latlng': f'{latitude},{longitude}'
        }
        data = self._make_request('reverse-geocode', params)
        return self._extract_address(data)

    def geocode(self, address, bounds=None, language='hi'):
        params = {
            'address': address,
            'language': language
        }
        if bounds:
            params['bounds'] = bounds
        data = self._make_request('geocode', params)
        return self._extract_location(data)

    def _extract_address(self, data):
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]['formatted_address']
        return 'No address found in the response.'

    def _extract_location(self, data):
        if 'geocodingResults' in data and len(data['geocodingResults']) > 0:
            return data['geocodingResults']
        return 'No location found in the response.'

    def display_geocoding_results(self, results):
        for result in results:
            formatted_address = result.get('formatted_address', 'N/A')
            location = result.get('geometry', {}).get('location', {})
            latitude = location.get('lat', 'N/A')
            longitude = location.get('lng', 'N/A')
            print(f'Formatted Address: {formatted_address}')
            print(f'Location: Latitude = {latitude}, Longitude = {longitude}')
            print('-' * 40)
