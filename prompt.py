def agent_prompt(name, city, state, weather, time):
    return {
        "role": "system",
        "content": f"""
        You are an intelligent bot designed to handle user queries and provide precise information. Select the appropriate tool for each query. You are responsible for identifying and solving user queries and reporting to the human with the help of given tools.
        
        You are speaking with {name} in {city}, {state}. The current weather is {weather}, and the time is {time}. Greet the user with a comment on the current weather using an emoji.
        -strictly follow
        Don't say what tool you are using just give the response directly.mandatory
        dont confirm the tool with user select the tool by yourself.mandatory
        other than greeting who should not process and give output by yourself you have to call the tool.mandatory
        don't confirm anything from the user.mandatory
        dont ask user to wait and dont share what is you are processing
        you have to call the tool.mandatory

        Available Tools(choose the tool by own don't ask this to user):
        
        - location_nearby_search: Search for nearby places (e.g., coffee shops).
        - location_search: Search for specific locations by name.
        - service_nearby_search: Find nearby services (e.g., plumbing).
        - weather_search: Get current weather information for a location.
        - local_events_search: Find events in a specified area.
        - flight_search: Find flights between two locations.
        - direction_search: Get directions between two places.
        - web_search: Fetch current events or updates.
        - news_search: Search for news updates.
        
        After selecting a tool, you will receive observations from the tool and provide a response to the user.
        
        Choose the tools automatically to solve the user's query. Your role is to facilitate a seamless interaction, ensuring user satisfaction and timely resolution of their queries by efficiently utilizing the provided tools and consulting the manager when necessary. Respond promptly to any tasks or input requests from the manager to ensure smooth operations.
        """
    }

tools = [
    {
        "type": "function",
        "function": {
            "name": "location_nearby_search",
            "description": "Search for nearby places of a specified type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "place_type": {
                        "type": "string",
                        "description": "Type of place (e.g., coffee shop, bus stop)."
                    }
                },
                "required": ["place_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "location_search",
            "description": "Search for specific locations by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "Name of the location."
                    }
                },
                "required": ["location_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "service_nearby_search",
            "description": "Search for nearby services of a specified type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_type": {
                        "type": "string",
                        "description": "Type of service (e.g., plumbing)."
                    }
                },
                "required": ["service_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "weather_search",
            "description": "Get current weather information for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "Name of the location."
                    }
                },
                "required": ["location_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "local_events_search",
            "description": "Find local events in a specified location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "Name of the location."
                    }
                },
                "required": ["location_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "flight_search",
            "description": "Search for flights between two locations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure_location": {
                        "type": "string",
                        "description": "Departure location."
                    },
                    "arrival_location": {
                        "type": "string",
                        "description": "Arrival location."
                    },
                    "departure_date": {
                        "type": "string",
                        "description": "Date of departure."
                    },
                    "return_date": {
                        "type": "string",
                        "description": "Date of return (optional)."
                    }
                },
                "required": ["departure_location", "arrival_location", "departure_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "direction_search",
            "description": "Get directions between two places.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_location": {
                        "type": "string",
                        "description": "Starting location will be alway default to user location."
                    },
                    "end_location": {
                        "type": "string",
                        "description": "Ending location."
                    }
                },
                "required": ["start_location", "end_location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Fetch current events or updates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "User query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "news_search",
            "description": "Search for news on a specified topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "News search query."
                    }
                },
                "required": ["query"]
            }
        }
    }
]
