import requests


class HereService:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def get_coordinates(self, address):
        url = f"https://geocode.search.hereapi.com/v1/geocode?q={address}&apiKey={self.api_key}"
        
        response = requests.get(url)
        json = response.json()
        
        return json["items"][0]["position"]
