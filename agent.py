from prompt import agent_prompt, tools
from llm import *
from functions import *
import geocoder
import json, os
from location import GeocodingClient, find_location
from datetime import datetime
import pytz
from pymongo import MongoClient
from database import *

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

def agent(prompt, user_name ,latitude, longitude):
    city, state = find_location(latitude, longitude)
    weather = "rainy"
    system_message = agent_prompt(user_name, city, state, weather, time)


    #history =get_history_from_worker(conversation_history,conversation_id)
    messages = [system_message] + [{"role": "user", "content": prompt}]
    intent, map_url = None, None
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
                    pass
                elif function_name == "direction_search":
                    intent = "direction_search"
                    start, end = function_args.get("start_location"),  function_args.get("end_location")
                    summary, google_map_url = direction_tool(start, end)
                    map_url = google_map_url
                    messages.append({"role": "user", "content":f"Observation :/n{summary}"})
                elif function_name == "location_search":
                    intent = "location_search"
                    pass
                elif function_name == "service_nearby_search":
                    intent = "service_nearby_search"
                    pass
                elif function_name == "weather_search":
                    intent = "weather_search"
                    pass
                elif function_name == "local_events_search":
                    intent = "local_events_search"
                    pass
                elif function_name == "flight_search":
                    intent = "flight_search"
                    pass
                elif function_name == "local_news_search":
                    intent = "local_news_search"
                    pass
                elif function_name == "web_search":
                    intent = "web_search"
                    inputs = function_args.get("query")
                    web_search = search(inputs)
                    messages.append({"role": "user", "content":f"Observation :/n{web_search}"})
        else:
            #insert_conversations(conversation_history, prompt, response_message.content, conversation_id, latitude, longitude, time, map_url, intent)
            return {
                "completion" : response_message.content,
                #"conversation_id" : conversation_id,
                "intent" : intent,
                "map_url" : map_url
            }
                                
    
x = agent("what is a distance between madurai to chennai", "gokul", 11.7910866,77.778496)
print(x)
print(x["completion"])