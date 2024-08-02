from googleapiclient.discovery import build
import os

def search(search_term):
    search_result = ""
    service = build("customsearch", "v1", developerKey=os.environ.get("GOOGLE_API_KEY"))
    res = service.cse().list(q=search_term, cx=os.environ.get("GOOGLE_CSE_ID"), num = 10).execute()
    for result in res['items']:
        search_result = search_result + result['snippet']
    return search_result

import serpapi


def direction_tool(start_location, end_location):
    params = {
    "engine": "google_maps_directions",
    "hl": "en",
    "start_addr": start_location,
    "end_addr": end_location
    }
    client = serpapi.Client(api_key=os.environ.get("serph_api"))
    search = client.search(params)
    results = search.as_dict()
    google_map_direction_url =  results['search_metadata']['google_maps_directions_url']

    summary = f"""
    Places Info
    """
    for place in results.get('places_info', []):
        summary += f"""
    {place.get('address', 'N/A')}
    Data ID: {place.get('data_id', 'N/A')}
    GPS Coordinates: Latitude {place['gps_coordinates'].get('latitude', 'N/A')}, Longitude {place['gps_coordinates'].get('longitude', 'N/A')}
    """

    summary += """
    Directions (Two-Wheeler)
    """
    for direction in results.get('directions', []):
        if direction.get('travel_mode') == 'Two-wheeler':
            summary += f"""
    Total Distance: {direction.get('formatted_distance', 'N/A')}
    Total Duration: {direction.get('formatted_duration', 'N/A')}
    Typical Duration Range: {direction.get('typical_duration_range', 'N/A')}
    {' '.join(direction.get('extensions', []))}

    Detailed Trips:
    """
            for trip in direction.get('trips', []):
                summary += f"""
    {trip.get('title', 'N/A')}
    Distance: {trip.get('formatted_distance', 'N/A')}
    Duration: {trip.get('formatted_duration', 'N/A')}
    Key Steps:
    """
                for detail in trip.get('details', []):
                    summary += f"{detail.get('title', 'N/A')}\n"

    summary += """
    Other Travel Modes
    """
    for direction in results.get('directions', []):
        if direction.get('travel_mode') != 'Two-wheeler':
            summary += f"""
    {direction.get('travel_mode', 'N/A').capitalize()}
    Distance: {direction.get('formatted_distance', 'N/A')}
    Duration: {direction.get('formatted_duration', 'N/A')}
    """
            if 'typical_duration_range' in direction:
                summary += f"Typical Duration Range: {direction.get('typical_duration_range', 'N/A')}\n"
            if 'via' in direction:
                summary += f"Route: {direction.get('via', 'N/A')}\n"
            if direction.get('travel_mode') == 'Transit':
                summary += f"Route: {direction['trips'][0].get('title', 'N/A')}\nStops: {', '.join([stop.get('name', 'N/A') for stop in direction['trips'][0].get('stops', [])])}\n"
            if direction.get('travel_mode') == 'Walking':
                summary += f"Duration: {direction.get('formatted_duration', 'N/A')}"

    return summary, google_map_direction_url
