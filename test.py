import requests

headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer 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'
    }
url = 'https://incletech-incle-ai71.hf.space/agent'

def send_request(prompt, conversation_id, user_name, latitude, longitude):
    payload = {
        'prompt': prompt,
        'conversation_id': conversation_id,
        'user_name': user_name,
        'latitude': latitude,
        'longitude': longitude
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

# Example usage
response = send_request(
    prompt="whats the distance between chennai to madurai",
    conversation_id="4v4955t45",
    user_name="Gokul",
    latitude=11.7910873,
    longitude=77.7990956,
)

print(response)
