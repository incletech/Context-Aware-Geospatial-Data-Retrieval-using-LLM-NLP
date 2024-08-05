# import os
# import logging
# from googleapiclient.discovery import build
# from opencage.geocoder import OpenCageGeocode
# from groq import Groq
# import serpapi

# class agent_tools:
#     def __init__(self):
#         self.client = serpapi.Client(api_key=os.environ.get("serph_api"))
#         self.google_api_key = os.environ.get("GOOGLE_API_KEY")
#         self.google_cse_id = os.environ.get("GOOGLE_CSE_ID")
#         self.groq_client = Groq(api_key=os.getenv("groq_api"))

#     def web_search(self, search_term):
#         search_result = ""
#         service = build("customsearch", "v1", developerKey=self.google_api_key)
#         res = service.cse().list(q=search_term, cx=self.google_cse_id, num=10).execute()
#         for result in res['items']:
#             search_result += result['snippet']
#         return search_result

#     def direction_tool(self, start_location, end_location):
#         params = {
#             "engine": "google_maps_directions",
#             "hl": "en",
#             "start_addr": start_location,
#             "end_addr": end_location
#         }
#         search = self.client.search(params)
#         results = search.as_dict()
#         google_map_direction_url = results['search_metadata']['google_maps_directions_url']
#         summary = self._format_directions(results)
#         return summary, google_map_direction_url

#     def _format_directions(self, results):
#         summary = "Places Info\n"
#         for place in results.get('places_info', []):
#             summary += f"""
#             {place.get('address', 'N/A')}
#             Data ID: {place.get('data_id', 'N/A')}
#             GPS Coordinates: Latitude {place['gps_coordinates'].get('latitude', 'N/A')}, Longitude {place['gps_coordinates'].get('longitude', 'N/A')}
#             """

#         summary += "\nDirections (Two-Wheeler)\n"
#         for direction in results.get('directions', []):
#             if direction.get('travel_mode') == 'Two-wheeler':
#                 summary += self._format_direction_details(direction)
#         summary += "\nOther Travel Modes\n"
#         for direction in results.get('directions', []):
#             if direction.get('travel_mode') != 'Two-wheeler':
#                 summary += self._format_other_travel_modes(direction)
#         return summary

#     def _format_direction_details(self, direction):
#         details = f"""
#         Total Distance: {direction.get('formatted_distance', 'N/A')}
#         Total Duration: {direction.get('formatted_duration', 'N/A')}
#         Typical Duration Range: {direction.get('typical_duration_range', 'N/A')}
#         {' '.join(direction.get('extensions', []))}

#         Detailed Trips:
#         """
#         for trip in direction.get('trips', []):
#             details += f"""
#             {trip.get('title', 'N/A')}
#             Distance: {trip.get('formatted_distance', 'N/A')}
#             Duration: {trip.get('formatted_duration', 'N/A')}
#             Key Steps:
#             """
#             for detail in trip.get('details', []):
#                 details += f"{detail.get('title', 'N/A')}\n"
#         return details

#     def _format_other_travel_modes(self, direction):
#         details = f"""
#         {direction.get('travel_mode', 'N/A').capitalize()}
#         Distance: {direction.get('formatted_distance', 'N/A')}
#         Duration: {direction.get('formatted_duration', 'N/A')}
#         """
#         if 'typical_duration_range' in direction:
#             details += f"Typical Duration Range: {direction.get('typical_duration_range', 'N/A')}\n"
#         if 'via' in direction:
#             details += f"Route: {direction.get('via', 'N/A')}\n"
#         if direction.get('travel_mode') == 'Transit':
#             details += f"Route: {direction['trips'][0].get('title', 'N/A')}\nStops: {', '.join([stop.get('name', 'N/A') for stop in direction['trips'][0].get('stops', [])])}\n"
#         if direction.get('travel_mode') == 'Walking':
#             details += f"Duration: {direction.get('formatted_duration', 'N/A')}"
#         return details

#     def news_search(self, topic):
#         params = {
#             "api_key": os.environ.get("serph_api"),
#             "engine": "bing_news",
#             "q": topic
#         }
#         search = self.client.search(params)
#         results = search.as_dict()
#         news = self._format_news(results)
#         return news

#     def _format_news(self, results):
#         news = "news content\n"
#         for i, result in enumerate(results["organic_results"]):
#             news += f"""
#             Title: {result["title"]}
#             Source: {result["source"]}
#             Link: {result["link"]}
#             Date: {result["date"]}
#             """
#         return news

#     def local_event(self, location):
#         params = {
#             "api_key": os.environ.get("serph_api"),
#             "engine": "google_events",
#             "q": f"Events in {location}"
#         }
#         search = self.client.search(params)
#         results = search.as_dict()
#         events, google_map_direction_url = self._format_local_events(results)
#         return events, google_map_direction_url

#     def _format_local_events(self, results):
#         events = "local events\n"
#         for i in range(5):
#             event = results["events_results"][i]
#             title = event['title']
#             date_time = event['date']['when']
#             address = ', '.join(event['address'])
#             ticket_link = event['link']
#             map_link = event['event_location_map']['link']
#             events += f"""
#             Title: {title}
#             Date and Time: {date_time}
#             Address: {address}
#             Ticket Link: {ticket_link}
#             Map: {map_link}
#             """
#         google_map_direction_url = results.get('search_metadata', {}).get('google_events_url', 'N/A')
#         return events, google_map_direction_url

#     def weather_search(self, location):
#         params = {
#             "engine": "google",
#             "q": "weather",
#             "location": location,
#             "google_domain": "google.com",
#             "gl": "us",
#             "hl": "en"
#         }
#         search = self.client.search(params)
#         results = search.as_dict()
#         weather_details = self._format_weather(results)
#         return weather_details

#     def _format_weather(self, results):
#         weather_details = {
#             "temperature": results["answer_box"]["temperature"],
#             "unit": results["answer_box"]["unit"],
#             "precipitation": results["answer_box"]["precipitation"],
#             "humidity": results["answer_box"]["humidity"],
#             "wind": results["answer_box"]["wind"],
#             "location": results["answer_box"]["location"],
#             "date": results["answer_box"]["date"],
#             "weather": results["answer_box"]["weather"]
#         }
#         return weather_details

#     def code(self, airport):
#         link = "https://www.nationsonline.org/oneworld/IATA_Codes/airport_code_list.htm"
#         prompt = f"I'll give you the airport name you have to convert that to The International Air Transport Association's (IATA) Location Identifier is a unique 3-letter code (also commonly known as IATA code) used in aviation and also in logistics to identify an airport for your reference I'll give the data of the code {link}. For example, JFK is the IATA code for, you might know it, New York's John F. Kennedy International Airport, just return code alone not any other text.You should give it more accurately"

#         chat_completion = self.groq_client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",
#                     "content": prompt
#                 },
#                 {
#                     "role": "user",
#                     "content": airport,
#                 }
#             ],
#             model="llama3-70b-8192",
#         )
#         return chat_completion.choices[0].message.content

#     def flights(self, departure, arrival, outbound_date, return_date):
#         departure_code = self.code(departure)
#         arrival_code = self.code(arrival)
#         params = {
#             "api_key": os.environ.get("serph_api"),
#             "engine": "google_flights",
#             "hl": "en",
#             "gl": "in",
#             "departure_id": departure_code,
#             "arrival_id": arrival_code,
#             "outbound_date": outbound_date,
#             "return_date": return_date,
#             "currency": "INR"
#         }
#         try:
#             search = self.client.search(params)
#             results = search.as_dict()
#             summary, reference_url = self._format_flights(results)
#             return summary, reference_url
#         except Exception as e:
#             return f"An error occurred: {e}"

#     def _format_flights(self, results):
#         summary = "flights\n"
#         for flight in results.get('best_flights', []):
#             summary += f"""
#             Airline: {flight['flights'][0].get('airline', 'N/A')}
#             Flight Number: {flight['flights'][0].get('flight_number', 'N/A')}
#             Departure Airport: {flight['flights'][0]['departure_airport'].get('name', 'N/A')} ({flight['flights'][0]['departure_airport'].get('id', 'N/A')})
#             Departure Time: {flight['flights'][0]['departure_airport'].get('time', 'N/A')}
#             Arrival Airport: {flight['flights'][0]['arrival_airport'].get('name', 'N/A')} ({flight['flights'][0]['arrival_airport'].get('id', 'N/A')})
#             Arrival Time: {flight['flights'][0]['arrival_airport'].get('time', 'N/A')}
#             Duration: {flight['flights'][0].get('duration', 'N/A')} minutes
#             Airplane: {flight['flights'][0].get('airplane', 'N/A')}
#             Total Duration: {flight.get('total_duration', 'N/A')} minutes
#             Carbon Emissions: {flight['carbon_emissions'].get('this_flight', 'N/A')} kg (difference: {flight['carbon_emissions'].get('difference_percent', 'N/A')}% compared to typical)
#             Price: ₹{flight.get('price', 'N/A')}
#             """
#         reference_url = results.get('search_metadata', {}).get('google_flights_url', 'N/A')
#         return summary, reference_url

#     def local_search(self, query, latitude, longitude, zoom=10):
#         params = {
#             "engine": "google_maps",
#             "type": "search",
#             "google_domain": "google.com",
#             "q": query,
#             "ll": f"@{latitude},{longitude},{zoom}z",
#             "hl": "en"
#         }
#         search = self.client.search(params)
#         results = search.as_dict()
#         summary, google_map_direction_url = self._format_local_search(results)
#         return summary, google_map_direction_url

#     def _format_local_search(self, results):
#         summary = ""
#         for place in results.get('local_results', []):
#             summary += f"""
#             {place.get('position', 'N/A')}. {place.get('title', 'N/A')}
#             - Place ID: {place.get('place_id', 'N/A')}
#             - Data ID: {place.get('data_id', 'N/A')}
#             - Rating: {place.get('rating', 'N/A')}
#             - Reviews: {place.get('reviews', 'N/A')}
#             - Type: {place.get('type', 'N/A')}
#             - Address: {place.get('address', 'N/A')}
#             - Open State: {place.get('open_state', 'N/A')}
#             - Phone: {place.get('phone', 'N/A')}
#             - User Review: {place.get('user_review', 'N/A')}
#             """
#         google_map_direction_url = results.get('search_metadata', {}).get('google_maps_url', 'N/A')
#         return summary, google_map_direction_url

from googleapiclient.discovery import build
import os
from opencage.geocoder import OpenCageGeocode
from groq import Groq
import serpapi
import re
from urllib.parse import urlencode, unquote
import os
import itertools


# serph_key = [
#     os.getenv("serph_api"),   
#     os.getenv("serph_api1")
# ]

# serph_key_cycle = itertools.cycle(serph_key)

client = serpapi.Client(api_key=os.getenv("serph_api"))

def web_search(search_term):
    search_result = ""
    service = build("customsearch", "v1", developerKey=os.environ.get("GOOGLE_API_KEY"))
    res = service.cse().list(q=search_term, cx=os.environ.get("GOOGLE_CSE_ID"), num = 10).execute()
    for result in res['items']:
        search_result = search_result + result['snippet']
    return search_result

#emb
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
    google_map_direction_url = convert_to_embed_url_direction(google_map_direction_url)

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


def news_search(topic):
    params = {
    "engine": "bing_news",
    "q": topic
    }
    search = client.search(params)
    results = search.as_dict()
    final=results["organic_results"][0]
    news=f"""
    Show the all major informations to use
    news content
    """
    for i in range(len(results["organic_results"])):
        final=results["organic_results"][i]
        print("Title:",final["title"])
        print("Source:",final["source"])
        print("Link:",final["link"])
        print("Date:",final["date"])
        news+=f"""\nTitle:{final["title"]},\nSource:{final["source"]},\nLink:{final["link"]},\nDate:{final["date"]}\n"""

    return news

def local_event(location):
    params = {
        "engine": "google_events",
        "q": f"Events in {location}"
    }
    search = client.search(params)
    results = search.as_dict()
    search_metadata = results.get('search_metadata', {})
    google_map_direction_url = search_metadata.get('google_events_url', 'N/A')
    
    if 'events_results' not in results or not results['events_results']:
        return "There are no events in your location.", google_map_direction_url

    events = "Local events:\n"
    for i in range(min(5, len(results["events_results"]))): 
        event = results["events_results"][i]
        title = event['title']
        date_time = event['date']['when']
        address = ', '.join(event['address'])
        ticket_link = event['link']
        map_link = event['event_location_map']['link']
        events += f"\nTitle: {title}\nDate and Time: {date_time}\nAddress: {address}\nTicket Link: {ticket_link}\nMap: {map_link}\n"

    return events, google_map_direction_url


def weather_search(location):   
    params = {
    "engine": "google",
    "q": "weather",
    "location": location,
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en"
    }
    search = client.search(params)
    results = search.as_dict()
    print(results)
    weather_details = {
        "temperature": results["answer_box"]["temperature"],
        "unit": results["answer_box"]["unit"],
        "precipitation": results["answer_box"]["precipitation"],
        "humidity": results["answer_box"]["humidity"],
        "wind": results["answer_box"]["wind"],
        "location": results["answer_box"]["location"],
        "date": results["answer_box"]["date"],
        "weather": results["answer_box"]["weather"]
    }
    return weather_details

def code(airport):
    client = Groq(
    api_key=os.getenv("groq_api"),
    )
    link="https://www.nationsonline.org/oneworld/IATA_Codes/airport_code_list.htm"
    prompt=f"I'll give you the airport name you have to convert that to The International Air Transport Association's (IATA) Location Identifier is a unique 3-letter code (also commonly known as IATA code) used in aviation and also in logistics to identify an airport for your reference I'll give the data of the code {link}. For example, JFK is the IATA code for, you might know it, New York's John F. Kennedy International Airport,just return code alone not any other text.You should give it more accurately"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": airport,
            }
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content

def flights(departure, arrival, outbound_date, return_date=None):
    departure = code(departure)
    print(departure)
    arrival = code(arrival)
    print(arrival)
    params = {
        "engine": "google_flights",
        "hl": "en",
        "gl": "in",
        "departure_id": departure,
        "arrival_id": arrival,
        "outbound_date": outbound_date,
        "currency": "INR"
    }
    if return_date:
        params["return_date"] = return_date

    try:
        search = client.search(params)
        results = search.as_dict()
        search_metadata = results.get('search_metadata', {})
        reference_url = search_metadata.get('google_flights_url', 'N/A')
        summary = "flights\n"
        for flight in results.get('best_flights', []):
            summary += f"""
              Airline: {flight['flights'][0].get('airline', 'N/A')}
              Flight Number: {flight['flights'][0].get('flight_number', 'N/A')}
              Departure Airport: {flight['flights'][0]['departure_airport'].get('name', 'N/A')} ({flight['flights'][0]['departure_airport'].get('id', 'N/A')})
              Departure Time: {flight['flights'][0]['departure_airport'].get('time', 'N/A')}
              Arrival Airport: {flight['flights'][0]['arrival_airport'].get('name', 'N/A')} ({flight['flights'][0]['arrival_airport'].get('id', 'N/A')})
              Arrival Time: {flight['flights'][0]['arrival_airport'].get('time', 'N/A')}
              Duration: {flight['flights'][0].get('duration', 'N/A')} minutes
              Airplane: {flight['flights'][0].get('airplane', 'N/A')}

              Total Duration: {flight.get('total_duration', 'N/A')} minutes
              Carbon Emissions: {flight['carbon_emissions'].get('this_flight', 'N/A')} kg (difference: {flight['carbon_emissions'].get('difference_percent', 'N/A')}% compared to typical)
              Price: ₹{flight.get('price', 'N/A')}
              """
        return summary, reference_url

    except Exception as e:
        return f"An error occurred: {e}"

#emb
def local_search(query, latitude, longitude, zoom = 10):
    params = {
    "engine": "google_maps",
    "type": "search",
    "google_domain": "google.com",
    "q": query,
    "ll": f"@{latitude},{longitude},{zoom}z",
    "hl": "en"
    }

    search = client.search(params)
    results = search.as_dict()
    print(results)
    
    summary = "Show the all major informations to use. \n"
    
    search_metadata = results.get('search_metadata', {})
    google_map_direction_url = search_metadata.get('google_maps_url', None)

    if google_map_direction_url:
       google_map_direction_url = convert_to_embed_url(google_map_direction_url)
        
    local_results = results.get('local_results', [])

    for place in local_results:
        summary += f"""
{place.get('position', 'N/A')}. {place.get('title', 'N/A')}
  - Data ID: {place.get('data_id', 'N/A')}
  - Rating: {place.get('rating', 'N/A')}
  - Reviews: {place.get('reviews', 'N/A')}
  - Type: {place.get('type', 'N/A')}
  - Address: {place.get('address', 'N/A')}
  - Open State: {place.get('open_state', 'N/A')}
  - Phone: {place.get('phone', 'N/A')}
  - User Review: {place.get('user_review', 'N/A')}
        """

    return summary, google_map_direction_url

def convert_to_embed_url(url):
    query_pattern = re.compile(r'maps/search/([^/]+)')
    query_match = query_pattern.search(url)
    if not query_match:
        raise ValueError("Invalid URL format: missing search query")
    query = query_match.group(1)
    coords_pattern = re.compile(r'@(-?\d+\.\d+),(-?\d+\.\d+),(\d+)z')
    coords_match = coords_pattern.search(url)
    if not coords_match:
        raise ValueError("Invalid URL format: missing coordinates or zoom level")
    
    latitude = coords_match.group(1)
    longitude = coords_match.group(2)
    zoom = coords_match.group(3)
    embed_url = "https://www.google.com/maps/embed/v1/place?" + urlencode({
        'q': query,
        'center': f'{latitude},{longitude}',
        'zoom': zoom,
        'key': os.environ.get("google_map")
    })
    
    return embed_url

def convert_to_embed_url_direction(url):
    dir_pattern = re.compile(r'maps/dir/([^/]+)/([^/]+)/data')
    dir_match = dir_pattern.search(url)
    if not dir_match:
        raise ValueError("Invalid URL format: missing directions path")
    
    start_location = unquote(dir_match.group(1))
    end_location = unquote(dir_match.group(2))
    travel_mode_match = re.search(r'(\d{2})(\?hl=en)?$', url)
    travel_mode = "driving"
    if travel_mode_match and travel_mode_match.group(1) == "3e6":
        travel_mode = "two_wheeler"
    embed_url = "https://www.google.com/maps/embed/v1/directions?" + urlencode({
        'origin': start_location,
        'destination': end_location,
        'mode': travel_mode,
        'key': os.environ.get("google_map")
    })
    
    return embed_url