import requests
api = "TESTTESTSETTESTTESTTEST"
def find_location(query, api_key):
    params = {
        "q": query,
        "limit": 5,  # Limit the number of locations returned
        "engine": "google",
        "api_key": api_key,
    }
    response = requests.get("https://serpapi.com/locations.json", params=params)
    
    if response.status_code == 200:
        locations = response.json()
        if locations:
            print("\n[+] Possible Locations Found:")
            for location in locations:
                # Safely get keys with default values to avoid KeyError
                location_id = location.get('id', 'N/A')
                name = location.get('name', 'N/A')
                country = location.get('country', 'N/A')
                canonical_name = location.get('canonical_name', 'N/A')
                
                print(f"ID: {location_id}, Name: {name}, Country: {country}, Canonical Name: {canonical_name}")
        else:
            print("[-] No locations found for the query.")
    else:
        print(f"[!] Error fetching locations: {response.status_code}, {response.text}")

if __name__ == "__main__":
    api_key = api
    location_query = input("[+] Enter the location query (e.g., 'New York'): ")
    find_location(location_query, api_key)
