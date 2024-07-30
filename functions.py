import serpapi, os

def search(query,location):
    params = {
    "api_key": os.getenv("serph_api"),
    "engine": "google_maps",
    "type": "search",
    "google_domain": "google.com",
    "q": query,
    "ll": location,
    "hl": "en"
    }
    client = serpapi.Client(api_key=os.getenv("serph_api"))
    search = client.search(params)
    results = search.as_dict()
    title_list=[]
    address_list=[]
    output=[]
    if 'local_results' in results and 'search_metadata' in results and 'google_maps_url' in results['search_metadata']:
            for result in results['local_results']:
                title = result.get('title', 'No Title')
                output.append(title)
                address = result.get('address', 'No Address')
                output.append(address)
                # print(title_list)
                # print(address_list)
    return output
            




