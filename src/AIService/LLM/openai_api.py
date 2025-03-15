import requests
import json
import os

def ask_custom(prompt, files, model, api, key):
    # Prepare the API endpoint
    url = f"{api.rstrip('/')}/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    # Prepare the files for submission if provided
    file_contents = []
    if files and isinstance(files, list):
        for file_path in files:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    file_name = os.path.basename(file_path)
                    file_contents.append(f"File: {file_name}\n\n{content}")

        # Add file contents to prompt if available
        if file_contents:
            file_context = "\n\n".join(file_contents)
            prompt = (
                f"Context from files:\n\n{file_context}\n\n---\n\nQuestion: {prompt}"
            )

    # Prepare the request payload
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": True,
    }

    # process streaming response
    response = requests.post(url, headers=headers, json=payload, stream=True)
    result = ""
    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8")
            if line.startswith("data: "):
                line = line[6:]
                if line == "[DONE]":
                    break
                try:
                    json_response = json.loads(line)
                    content = json_response["choices"][0]["delta"].get("content", "")
                    result += content
                    # print(content, end="", flush=True)

                    if json_response["choices"][0]["finish_reason"] == "stop":
                        # print("<STOP>")
                        break

                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {line}")
    
    return result.strip() if result else None


def custom_ask(api, key, model):
    def wrapper(prompt, files=[]):
        return ask_custom(prompt, files, model, api, key)
    
    return wrapper

