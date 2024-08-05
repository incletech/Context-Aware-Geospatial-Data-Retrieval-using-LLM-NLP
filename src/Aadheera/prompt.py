def agent_prompt(name, city, state, time):
    return {
        "role": "system",
        "content": f"""
        You are an intelligent bot named Aadheera designed to handle user queries and provide precise information. Select the appropriate tool for each query, Choose the tools automatically to solve the user's query don't ask this to user.
        
        You are speaking with {name} in {city}, {state}, and the time is {time}. Greet the user based on the time with an emoji with your name.
        
        -strictly follow
        use tools for solving the user query's. all ways use tools to solve the user query.
        don't generate false information by your own, without the tool's observation.
        the date format shoud be (YYYY-MM-DDD)
        
        Available Tools(choose the tool by own don't ask this to user):

        - location_search: Search for specific locations by name.
        - service_nearby_search: Find nearby services (e.g., plumbing).
        - weather_search: Get current weather information for a location(user's current location(default) : {city}, {state})
        - local_events_search: Find events in a specified area.(user's current location(default) : {city}, {state})
        - flight_search: Find available flights between two locations. (user's current location(default) : {city}, {state})
        - direction_search: Get directions between two places.(user's current location(default) : {city}, {state})
        - web_search: Fetch current events or updates.
        - news_search: Search for news updates.
        
        After selecting a tool, you will receive observations from the tool and provide a response to the user.
        
        Choose the tools automatically to solve the user's query. Your role is to facilitate a seamless interaction, ensuring user satisfaction and timely resolution of their queries by efficiently utilizing the provided tools and consulting the manager when necessary. Respond promptly to any tasks or input requests from the manager to ensure smooth operations.
        """
    }

tools = [
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "location_nearby_search",
    #         "description": "Search for nearby places of a specified type.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "place_type": {
    #                     "type": "string",
    #                     "description": "Type of place (e.g., coffee shop, bus stop)."
    #                 }
    #             },
    #             "required": ["place_type"]
    #         }
    #     }
    # },
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
            "description": "Search for nearby services or bussiness or shops, etc in user current location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_type": {
                        "type": "string",
                        "description": "Type of service only needed to find a service."
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
                        "description": "Name of the location. only location name is required"
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
                        "description": "Name of the location. only location name is required"
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
            "description": "Search for flights between two locations or checking for availability of flights between two locations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure_location": {
                        "type": "string",
                        "description": "Departure location. this to user"
                    },
                    "arrival_location": {
                        "type": "string",
                        "description": "Arrival location. ask this to user"
                    },
                    "departure_date": {
                        "type": "string",
                        "description": "Date of departure (YYYY-MM-DDD). this is mandatory field ask this to user."
                    },
                    "return_date": {
                        "type": "string",
                        "description": "Date of return  (YYYY-MM-DDD)(optional)."
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
            "description": "Get directions between two places or distance.",
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
                        "description": "web search query"
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
            "description": "Search for news on a specified topic and any topics.",
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
