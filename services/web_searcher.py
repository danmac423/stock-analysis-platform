import os
import requests
from dotenv import load_dotenv

load_dotenv()

class WebSearcher:
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.base_url = "https://google.serper.dev/search"

    def search(self, query: str, num_results: int = 5) -> list:
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query
        }

        response = requests.post(self.base_url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Serper API error: {response.text}")

        data = response.json()
        results = data.get("organic", [])[:num_results]

        return [
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            }
            for item in results
        ]
