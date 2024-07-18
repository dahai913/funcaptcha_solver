from curl_cffi import requests


class YesCaptchaAPI:
    def __init__(self, client_key):
        self.client_key = client_key
        self.create_task_url = 'https://api.yescaptcha.com/createTask'

    def create_task(self, image_base64, question):
        data = {
            "clientKey": self.client_key,
            "task": {
                "type": "FunCaptchaClassification",
                "image": image_base64,
                "question": question
            },
            "softID": 23225
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(self.create_task_url, json=data, headers=headers)
            return response.json()["solution"]["objects"][0]
        except:
            raise Exception("Failed to create task:", response.text)
