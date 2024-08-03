def convert_json_to_text_data(json_data):
    results = json_data.as_dict()
    summary = ""

    search_metadata = results.get('search_metadata', {})
    summary += f"""
Search Metadata:
  ID: {search_metadata.get('id', 'N/A')}
  Status: {search_metadata.get('status', 'N/A')}
  JSON Endpoint: {search_metadata.get('json_endpoint', 'N/A')}
  Created At: {search_metadata.get('created_at', 'N/A')}
  Processed At: {search_metadata.get('processed_at', 'N/A')}
  Google Maps URL: {search_metadata.get('google_maps_url', 'N/A')}
  Raw HTML File: {search_metadata.get('raw_html_file', 'N/A')}
  Total Time Taken: {search_metadata.get('total_time_taken', 'N/A')}
    """

    search_parameters = results.get('search_parameters', {})
    summary += f"""
Search Parameters:
  Engine: {search_parameters.get('engine', 'N/A')}
  Type: {search_parameters.get('type', 'N/A')}
  Query: {search_parameters.get('q', 'N/A')}
  Location: {search_parameters.get('ll', 'N/A')}
  Google Domain: {search_parameters.get('google_domain', 'N/A')}
  Language: {search_parameters.get('hl', 'N/A')}
    """

    search_information = results.get('search_information', {})
    summary += f"""
Search Information:
  Local Results State: {search_information.get('local_results_state', 'N/A')}
  Query Displayed: {search_information.get('query_displayed', 'N/A')}
    """

    local_results = results.get('local_results', [])
    for place in local_results:
        summary += f"""
{place.get('position', 'N/A')}. {place.get('title', 'N/A')}
  - Place ID: {place.get('place_id', 'N/A')}
  - Data ID: {place.get('data_id', 'N/A')}
  - Rating: {place.get('rating', 'N/A')}
  - Reviews: {place.get('reviews', 'N/A')}
  - Type: {place.get('type', 'N/A')}
  - Address: {place.get('address', 'N/A')}
  - Open State: {place.get('open_state', 'N/A')}
  - Phone: {place.get('phone', 'N/A')}
  - User Review: {place.get('user_review', 'N/A')}
        """
    return summary, g
