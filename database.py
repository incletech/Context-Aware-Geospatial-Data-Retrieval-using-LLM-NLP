import logging
def insert_conversations(collection, prompt, content, conversation_id, latitude, longitude, date, map_url, intent):
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
            "date": date,
            "map_url" : map_url,
            "intent" : intent
        }
    ]
    collection.insert_many(logs)

def get_history_from_worker(collection, conversation_id):
    try:
        query = {"conversation_id": conversation_id}
        projection = {"role": 1, "content": 1, "_id": 0}
        results = collection.find(query, projection).sort([("date", 1)])
        all_messages = list(results)
        return all_messages
    except Exception as e:
        logging.error(f"Failed to retrieve history from DB: {e}")
        return []