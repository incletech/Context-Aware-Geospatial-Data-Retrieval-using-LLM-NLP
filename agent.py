from prompt import *
from llm import *
from functions import *
import geocoder
import json, os
async def bot(prompt):
    input = "human input : " + prompt
    content= [{"role": "user", "content": input}]
    g = geocoder.ip('me')
    print("loc",', '.join([f'"{element}"' for element in g.latlng]))
    location=g.city and g.bbox
    system_prompt = await agent_prompt(location)
    message_agent=[system_prompt] + content
    agent_response= await llm_call(message_agent)
    print("agent_response",agent_response)
    if agent_response is None:
        raise ValueError("agent_response is None")

    # Parse the JSON response
    data = json.loads(agent_response)

    # Extract the value of 'tool' and store it in function_name
    function_name = data['tool']
    print(function_name)
    if function_name == "location_nearby_search":
        print(prompt)
        loc = ','.join([f'{element}' for element in g.latlng])
        # print(f'"@{loc},14z"')
        locz="@11.0055,76.9661,14z"
        loc1=f'"@{loc},14z"'
        print(loc1)
        output=search(prompt,locz)
        temp=[]
        for i in output:
            temp.append(i)
            if len(temp)>=10:
                break
            else:
                # print(i)
                pass
        # print(temp)
        human_response=await llm_response(temp)
        print(human_response)
        # print(output)
    elif function_name == "location_search":
        print(prompt)
        output="comming soon 1"
        print(output)
    elif function_name == "crop_data_search":
        print(prompt)
        output="comming soon 2"
        print(output)
    elif function_name == "service_nearby_search":
        print(prompt)
        output="comming soon 3"
        print(output)
    else:
        raise ValueError("Invalid tool name")

    return None
    