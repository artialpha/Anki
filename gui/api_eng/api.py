import json
import requests


class Api:
    def __init__(self, app_id, app_key, end_point, language_code):
        self.app_id = app_id
        self.app_key = app_key
        self.end_point = end_point
        self.language_code = language_code

    def word_json(self, word_id):
        url = "https://od-api.oxforddictionaries.com/api/v2/" + self.end_point + "/" + self.language_code + "/" + word_id.lower()
        r = requests.get(url, headers={"app_id": self.app_id, "app_key": self.app_key})
        return json.loads(r.text)
