import requests


class Refresh:
    def __init__(self) -> None:
        self.refresh_token = 'your_refresh_token_here'
        self.base_64_cred = 'base_64_encoded_client_id:client_secret'

    def refresh(self):
        
        uri = 'https://accounts.spotify.com/api/token'
        response = requests.post(uri, 
        data={
            "grant_type": "refresh_token",
            "refresh_token":self.refresh_token
            },
        headers={
            "Authorization": "Basic "+ self.base_64_cred
        })

        return response.json()["access_token"]
