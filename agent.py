from src.Aadheera.prompt import agent_prompt, tools
from src.Aadheera.llm import *
from src.Aadheera.functions import *
import geocoder
import json, os
from src.Aadheera.location import GeocodingClient
from datetime import datetime
import pytz
from pymongo import MongoClient
from src.Aadheera.database import *

mongo_client = MongoClient(os.getenv("mongo_db_connection_string"))
db = mongo_client["incle"]
conversation_history = db["falcon_conversation_history"]

india_tz = pytz.timezone('Asia/Kolkata')
current_time_india = datetime.now(india_tz)
time = current_time_india.strftime('%Y-%m-%d %H:%M:%S')

client = GeocodingClient()


falcon_completion = LlmModel.from_config("ai71", "tiiuae/falcon-180B-chat", 1, 8192)
llama_70b_tool_calling_completion = LlmModel.from_config("groq", "llama3-groq-70b-8192-tool-use-preview", 1, 8192)
llama_31_70b_completion = LlmModel.from_config("groq", "llama-3.1-70b-versatile", 0, 4000)

def agent_api(prompt, conversation_id, user_name ,latitude, longitude):

    history, city, state, weather_data, history_latitude, history_longitude = get_history_from_worker(conversation_history, conversation_id)

    if history:
        weather_data_string = f"temperature :{weather_data['temperature']}, wind :{weather_data['wind']}, humidity :{weather_data['humidity']}, weather: {weather_data['weather']}"
        print("old history")
        if latitude != history_latitude or longitude != history_longitude:
            print("new location")
            city, state = client.google_reverse_geocode(latitude, longitude)
            weather_data = weather_search(f"{city}, {state}")
            weather_data_string = f"temperature :{weather_data['temperature']}, wind :{weather_data['wind']}, humidity :{weather_data['humidity']}, weather: {weather_data['weather']}"

    else:
        print("no history")
        city, state = client.google_reverse_geocode(latitude, longitude)
        weather_data = weather_search(f"{city}, {state}")
        print(weather_data)
        weather_data_string = f"temperature :{weather_data['temperature']}, wind :{weather_data['wind']}, humidity :{weather_data['humidity']}, weather: {weather_data['weather']}"

    print(weather_data_string)    
    system_message = agent_prompt(user_name, city, state, weather_data_string, time)
    messages = [system_message] + history + [{"role": "user", "content": prompt}]
    intent, map_url, reference_url = None, None, None

    while True:
        response = llama_70b_tool_calling_completion.function_calling(messages=messages, tools=tools)
        response_message = response.choices[0].message
        print(response_message)
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                print(f"Function call: {function_name}")
                print(f"Function arguments: {function_args}")
                print("\n\n")


                if function_name == "location_nearby_search":
                    intent = "location_nearby_search"
                    query,location=function_args.get("service_type"),function_args.get("location_name")
                    summary, map_url= local_search(query, latitude, longitude, 15)
                    messages.append({"role": "user", "content":f"Observation :/n{summary}"})

                elif function_name == "direction_search":
                    intent = "direction_search"
                    start, end = function_args.get("start_location"),  function_args.get("end_location")
                    summary, map_url = direction_tool(start, end)
                    messages.append({"role": "user", "content":f"Observation :/n{summary}"})
                
                elif function_name == "location_search":
                    intent = "location_search"
                    inputs = function_args.get("location_name")
                    web_search = web_search(inputs)
                    messages.append({"role": "user", "content":f"Observation :/n{web_search}"})

                elif function_name == "service_nearby_search":
                    print("service")
                    intent = "service_nearby_search"
                    query,location=function_args.get("service_type"),function_args.get("location_name")
                    print("In")
                    summary, map_url= local_search(query, latitude, longitude, 15)
                    print("fun")
                    messages.append({"role": "user", "content":f"Observation :/n{summary}"})
                elif function_name == "weather_search":
                    intent = "weather_search"
                    inputs=function_args.get("location_name")
                    weather_result = str(weather_search(inputs))
                    messages.append({"role": "user", "content":f"Observation :/n{weather_result}"})
                elif function_name == "local_events_search":
                    intent = "local_events_search"
                    inputs=function_args.get("location_name")
                    local_events_search, reference_url = local_event(inputs)

                    messages.append({"role": "user", "content":f"Observation :/n{local_events_search}"})
                elif function_name == "flight_search":
                    intent = "flight_search"
                    departure_location = function_args.get("departure_location", None)
                    arrival_location = function_args.get("arrival_location", None)
                    departure_date = function_args.get("departure_date", None)
                    return_date = function_args.get("return_date", None)
                    flight_search, reference_url = flights(departure_location,arrival_location,departure_date,return_date)
                    messages.append({"role": "user", "content":f"Observation :/n{flight_search}"})
                elif function_name == "local_news_search":
                    intent = "local_news_search"
                    inputs=function_args.get("query")
                    local_news_search = news_search(inputs)
                    messages.append({"role": "user", "content":f"Observation :/n{local_news_search}"})
                elif function_name == "web_search":
                    intent = "web_search"
                    inputs = function_args.get("query")
                    web_search_result = web_search(inputs)
                    messages.append({"role": "user", "content":f"Observation :/n{web_search_result}"})
        else:
            insert_conversations(conversation_history, prompt, response_message.content, conversation_id, city, state,weather_data ,latitude, longitude, time, map_url, intent)
            return {
                "completion" : response_message.content,
                "conversation_id" : conversation_id,
                "intent" : intent,
                "map_url" : map_url,
                "reference_url" : reference_url
            }