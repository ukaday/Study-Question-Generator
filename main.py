import requests
import json

api_key = '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'
URL = "https://api.openai.com/v1/chat/completions"

payload = {
    "model": "gpt-3.5-turbo",
    "messages": [],
    "temperature": 1.0,
    "top_p": 1.0,
    "n": 1,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 0,
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


def main():
    running = True
    while running:
        message = input("User: ")

        if message == "!stop":
            break

        # adds user input to message history and sends
        payload["messages"].append({"role": "user", "content": f"{message}"})
        response = requests.post(URL, headers=headers, json=payload, stream=False)

        # checks if response was successful
        if response.status_code != 200:
            print("Request failed with status code:", response.status_code)
            pass

        # decodes response into dictionary
        response_data = json.loads(response.content.decode('utf-8'))
        # returns message contents, if none -> returns no message found instead of error
        response_message = response_data['choices'][0]['message'].get("content", "No response message found.")

        print(f"ChatGPT: {response_message}")
        tokens_used = response_data['usage'].get('total_tokens', "No token count found.")
        print(f"Tokens used: {tokens_used}")


if __name__ == '__main__':
    main()
