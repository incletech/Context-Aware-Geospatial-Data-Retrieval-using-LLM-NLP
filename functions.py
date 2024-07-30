import serpapi

def search(query,location):
    params = {
    "api_key": "3d48ec1b34dc9984498616e0c96660c30acc92441d257a575f70e5fa86cde75e",
    "engine": "google_maps",
    "type": "search",
    "google_domain": "google.com",
    "q": query,
    "ll": location,
    "hl": "en"
    }
    client = serpapi.Client(api_key="3d48ec1b34dc9984498616e0c96660c30acc92441d257a575f70e5fa86cde75e")
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
            




