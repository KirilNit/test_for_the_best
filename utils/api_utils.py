import requests


class ReqResAPI:

    def __init__(self, base_url=None):
        self.request = requests.Session()
        self.base_url = base_url or "https://reqres.in{}"

    def get(self, endpoint, parse):
        url = self.base_url.format(endpoint)
        response = self.request.get(url)
        if parse:
            return response.json()
        return response
