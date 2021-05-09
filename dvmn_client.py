import requests
from constants import DEVMAN_API_URL


class DevmanApi:

    def __init__(self, api_key):
        self.token = api_key
        self.base_url = DEVMAN_API_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {self.token}"
        })

    def get_reviews(self):
        url = self.base_url.format('user_reviews')
        res = requests.get(url, headers=self.session.headers)
        return res.json()

    def get_timestamp(self):
        url = self.base_url.format('long_polling')
        res = requests.get(url, headers=self.session.headers)
        if res.json()['status'] == 'timeout':
            return res.json()['timestamp_to_request']
        if res.json()['status'] == 'found':
            return res.json()['last_attempt_timestamp']
        return None

    def get_long_polling_reviews(self, timestamp=None):
        url = self.base_url.format('long_polling')
        res = requests.get(url, headers=self.session.headers, params={'timestamp': timestamp})
        return res.json()


