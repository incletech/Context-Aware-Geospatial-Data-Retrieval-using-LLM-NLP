from prompt import *
from llm import *
from functions import *
import geocoder
import json, os
from location import GeocodingClient

client = GeocodingClient()
completion = LlmModel.from_config("ai71", "tiiuae/falcon-180B-chat", 1, 1000)

def agent(prompt, user_name, latitude, longitude):
    address = client.reverse_geocode(latitude, longitude)
    system_message = agent_prompt(user_name, address)
    pass

