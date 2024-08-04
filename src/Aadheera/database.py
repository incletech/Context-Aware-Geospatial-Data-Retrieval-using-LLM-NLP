import logging
def insert_conversations(collection, prompt, content, conversation_id, city, state, weather, latitude, longitude, date, map_url, intent):
    logs = [
        {
            "role": "user",
            "content": prompt,
            "conversation_id": conversation_id,
            "latitude": latitude,
            "longitude": longitude,
            "date": date
        },
        {
            "role": "assistant",
            "content": content,
            "conversation_id": conversation_id,
            "latitude": latitude,
            "longitude": longitude,
            "location": {"city": city, "state": state},
            "weather": weather,
            "date": date,
            "map_url" : map_url,
            "intent" : intent
        }
    ]
    collection.insert_many(logs)


def get_history_from_worker(collection, conversation_id):
    try:
        query = {"conversation_id": conversation_id}
        projection = {"role": 1, "content": 1, "location": 1, "weather": 1, "latitude": 1, "longitude": 1, "_id": 0}
        results = collection.find(query, projection).sort([("date", 1)])
        all_messages = list(results)
        if not all_messages:
            return [], None, None, None, None, None 
        city = all_messages[-1]['location']['city']
        state = all_messages[-1]['location']['state']
        weather = all_messages[-1]['weather']
        latitude = all_messages[-1]['latitude']
        longitude = all_messages[-1]['longitude']
        history = [{'role': entry['role'], 'content': entry['content']} for entry in all_messages]
        return history, city, state, weather, latitude, longitude
    except Exception as e:
        logging.error(f"Failed to retrieve history from DB: {e}")
        return [], None, None, None, None, None  