import requests
import json


class GPTReceiver:
    def __init__(self):
        # gpt variables
        self.openai_api_key = ''
        self.URL = "https://api.openai.com/v1/chat/completions"
        self.payload = {
            "model": "gpt-3.5-turbo",
            "messages": [],
            "temperature": 1.0,
            "top_p": 1.0,
            "n": 1,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 0,
        }
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}"
        }

        # class variables
        self.current_response_data = None
        self.current_response_status = None

    def post_message(self, message):

        # adds user input to message history and sends
        self.payload["messages"].append({"role": "user", "content": f"{message}"})
        response = requests.post(self.URL, headers=self.headers, json=self.payload, stream=False)

        # checks if response was successful
        if response.status_code != 200:
            self.current_response_status = response.status_code
            return False

        # updates class variables
        self.current_response_status = response.status_code
        self.decode_response(response)

        # True denotes that the post was successful
        return True

    def get_status(self):
        # checks if status isn't successful
        if self.current_response_status != 200:
            return False, self.current_response_status

        return True, self.current_response_status

    def decode_response(self, response):
        # decodes response into dictionary
        self.current_response_data = json.loads(response.content.decode('utf-8'))

    def get_response_message(self):
        # checks if there is a current response
        if self.current_response_data is None:
            return None

        # returns response message contents
        return self.current_response_data['choices'][0]['message']['content']

    def get_response_tokens(self):
        # checks if there is a current response
        if self.current_response_data is None:
            return None

        # returns response token amount
        return self.current_response_data['usage']['total_tokens']

    def set_api_key(self, key):
        self.openai_api_key = str(key)
        self.headers['Authorization'] = f"Bearer {self.openai_api_key}"
