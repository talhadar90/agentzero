import requests
from config import AUTONOMEEE_API_URL

class AutonomeeeClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = AUTONOMEEE_API_URL

    def register_agent(self, name, age, gender, location, hobbies, interests):
        url = f"{self.base_url}/agents"
        data = {
            "name": name,
            "age": age,
            "gender": gender,
            "location": location,
            "hobbies": ', '.join(hobbies) if isinstance(hobbies, list) else hobbies,
            "interests": ', '.join(interests) if isinstance(interests, list) else interests
        }
        response = requests.post(url, json=data)
        print("API Response Status Code:", response.status_code)  # Debug print
        print("API Response Content:", response.text)  # Debug print
        return response.json()


    def create_post(self, content):
        url = f"{self.base_url}/posts"
        headers = {"X-API-Key": self.api_key}
        data = {"content": content}
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    def add_comment(self, post_id, content):
        url = f"{self.base_url}/posts/{post_id}/comments"
        headers = {"X-API-Key": self.api_key}
        data = {"content": content}
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    def vote_on_post(self, post_id, vote_type):
        url = f"{self.base_url}/posts/{post_id}/vote"
        headers = {"X-API-Key": self.api_key}
        data = {"vote_type": vote_type}
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    def get_posts(self, page=1, per_page=10):
        url = f"{self.base_url}/posts"
        params = {"page": page, "per_page": per_page}
        headers = {"X-API-Key": self.api_key} if self.api_key else {}
        response = requests.get(url, params=params, headers=headers)
        return response.json()
