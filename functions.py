from googleapiclient.discovery import build
import os
from opencage.geocoder import OpenCageGeocode
from groq import Groq
def search(search_term):
    search_result = ""
    service = build("customsearch", "v1", developerKey=os.environ.get("GOOGLE_API_KEY"))
    res = service.cse().list(q=search_term, cx=os.environ.get("GOOGLE_CSE_ID"), num = 10).execute()
    for result in res['items']:
        search_result = search_result + result['snippet']
    return search_result

import serpapi

client = serpapi.Client(api_key=os.environ.get("serph_api"))

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


def news_search(topic):
    params = {
    "api_key": os.environ.get("serph_api"),
    "engine": "bing_news",
    "q": topic
    }

    client = serpapi.Client(api_key=os.environ.get("serph_api"))
    search = client.search(params)
    results = search.as_dict()
    final=results["organic_results"][0]
    news=f"""
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
    "api_key": os.environ.get("serph_api"),
    "engine": "google_events",
    "q": f"Events in {location}"
    }

    client = serpapi.Client(api_key=os.environ.get("serph_api"))
    search = client.search(params)
    results = search.as_dict()
    # print(results["events_results"][0:5])
    events=f"""
    local events
    """
    for i in range(0,5):
        event = results["events_results"][i]  # Assuming you want to extract the first event
        title = event['title']
        date_time = event['date']['when']
        address = ', '.join(event['address'])
        ticket_link = event['link']
        map_link = event['event_location_map']['link']
        # Print the result
        print(f"Title: {title}")
        print(f"Date and Time: {date_time}")
        print(f"Address: {address}")
        print(f"Ticket Link: {ticket_link}")
        print(f"Map: {map_link}")
        events+=f"""\nTitle:{title},\nDate and Time:{date_time},\nAddress:{address},\nTicket Link: {ticket_link},\nMap:{map_link}\n"""

    return events
def weather_search(location):   
    params = {
    "api_key": os.environ.get("serph_api"),
    "engine": "google",
    "q": "weather",
    "location": location,
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en"
    }

    client = serpapi.Client(api_key=os.environ.get("serph_api"))
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
    print(weather_details)
    weather_report=f"""{weather_details}"""
    return weather_report
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
def flights(departure, arrival, outbound_date, return_date):
    departure = code(departure)
    arrival = code(arrival)
    params = {
        "api_key": os.environ.get("serph_api"),
        "engine": "google_flights",
        "hl": "en",
        "gl": "in",
        "departure_id": departure,
        "arrival_id": arrival,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": "INR"
    }

    try:
        client = serpapi.Client(api_key=os.environ.get("serph_api"))
        search = client.search(params)
        results = search.as_dict()
        print(results)
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
              Price: ${flight.get('price', 'N/A')}
              """
        return summary

    except Exception as e:
        return f"An error occurred: {e}"

def local_search(query,location):
    print(os.environ.get("serph_api"))
    params = {
    "engine": "google_maps",
    "type": "search",
    "google_domain": "google.com",
    "q": query,
    "ll": location,
    "hl": "en"
    }

    search = client.search(params)
    results = search.as_dict()
    # print(results)
    summary=f"""
    local results
    """
    for place in results.get('local_results', []):
        key = os.environ.get("OpenCage")
        geocoder = OpenCageGeocode(key)
        results = geocoder.reverse_geocode(place['gps_coordinates'].get('latitude'),place['gps_coordinates'].get('longitude'))
        summary += f"""
    Title: {place.get('title', 'N/A')}
    Rating: {place.get('rating', 'N/A')}
    Address: {place.get('address', 'N/A')}
    Open State: {place.get('open_state', 'N/A')}
    Hours: {place.get('hours', 'N/A')}
    Operating Hours: {place.get('operating_hours', 'N/A')}
    Phone: {place.get('phone', 'N/A')}
    Website: {place.get('website', 'N/A')}
    url = {results[0]['annotations']['OSM']['url']}
    """
    return summary
