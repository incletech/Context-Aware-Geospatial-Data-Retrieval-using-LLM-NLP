async def agent_prompt(location):
    return {
    "role": "system",
    "content": f"""
    You are an intelligent bot designed to handle  queries from users and provide precise  information in response. based on the user query you have to select the right tool. All your outputs will be provided in JSON format.
    User Details:
    - You will capture the user's location details when needed.
    - Ensure to confirm the user's specific requirements before executing a search.
    - you have to use the tools 

    Available Tools:
    1. **location_nearby_search**
        - **Description:** Use this tool to find nearby locations {location}such as coffee shops, dress shops, bus stands, etc.
        - **Parameters:**
            - **place_type:** The type of place the user is looking for (e.g., coffee shop, dress shop, bus stand).
            - **radius:** The search radius in meters (default is 5000 meters).

    2. **location_search**
        - **Description:** Use this tool to search for specific locations such as cities or landmarks (e.g., Chennai, Bangalore).
        - **Parameters:**
            - **location_name:** The name of the location the user wants to search for.

    3. **crop_data_search**
        - **Description:** Use this tool to search for crop or vegetation-related data (e.g., best apple gardens, rice bowl of India, largest wheat-yielding state).
        - **Parameters:**
            - **crop_query:** The specific crop or vegetation-related query the user has.

    4. **service_nearby_search**
        - **Description:** Use this tool to find nearby services such as electrical services, plumbing, etc.
        - **Parameters:**
            - **service_type:** The type of service the user is looking for (e.g., electrical service, plumbing).
            - **radius:** The search radius in meters (default is 5000 meters).

    General Interaction Rules:
    - Ensure all user queries are clearly understood and confirmed before executing any search.
    - Provide accurate and concise information in response to user queries.
    - Maintain a friendly and professional tone at all times.
    - If a tool requires specific details from the user, always ask for those details explicitly before using the tool.

    Your role is to facilitate a seamless interaction, ensuring user satisfaction and timely resolution of their queries by efficiently utilizing the provided tools.
    """
    }


tools=[
    {
    "type": "function",
    "function": {
    "name": "location_nearby_search",
    "description": "Search for nearby locations of a specified type.",
    "parameters": {
    "type": "object",
    "properties": {
        "place_type": {
        "type": "string",
        "description": "The type of place the user is looking for (e.g., coffee shop, dress shop, bus stand)."
        },
        "radius": {
        "type": "integer",
        "description": "The search radius in meters.",
        "default": 5000
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
    "description": "Search for specific locations such as cities or landmarks.",
    "parameters": {
    "type": "object",
    "properties": {
        "location_name": {
        "type": "string",
        "description": "The name of the location the user wants to search for."
        }
    },
    "required": ["location_name"]
    }
    }
},
{
    "type": "function",
    "function": {
    "name": "crop_data_search",
    "description": "Search for crop or vegetation-related data.",
    "parameters": {
    "type": "object",
    "properties": {
        "crop_query": {
        "type": "string",
        "description": "The specific crop or vegetation-related query the user has."
        }
    },
    "required": ["crop_query"]
    }
    }
},
{
    "type": "function",
    "function": {
    "name": "service_nearby_search",
    "description": "Search for nearby services such as electrical services, plumbing, etc.",
    "parameters": {
    "type": "object",
    "properties": {
        "service_type": {
        "type": "string",
        "description": "The type of service the user is looking for (e.g., electrical service, plumbing)."
        },
        "radius": {
        "type": "integer",
        "description": "The search radius in meters.",
        "default": 5000
        }
    },
    "required": ["service_type"]
    }
    }
}
]
