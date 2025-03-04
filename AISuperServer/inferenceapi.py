import requests
import json
import sys

class InferenceClient:
    def __init__(self, host: str = '0.0.0.0', port: str = '8080', api_key: str = None, multimodal: bool = False):
        self.baseurl = f"http://{host}:{port}"
        self.api_key = api_key
        self.header = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        self.multimodal = multimodal

    def CheckHealth(self):
        url = f'{self.baseurl}/api/health'
        try:
            if self.api_key is not None:
                response = requests.get(url=url, headers=self.header)
            else:
                response = requests.get(url, timeout=5) 
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def Query(self, query: str, systemprompt: str = None, image_path = None, stream: bool = False):
        if stream:
            return self.QueryStream(query=query, systemprompt=systemprompt)
        url = f"{self.baseurl}/api/inference"
        if self.multimodal and image_path:
            payload = {
                "query": query,
                "systemprompt": systemprompt,
                "image_path" : image_path,
                "stream": False
            }
        else:
            payload = {
                "query": query,
                "systemprompt": systemprompt,
                "stream": False
            }
        try:
            if self.api_key is not None:
                response = requests.post(url=url, headers=self.header, json=payload)
            else:
                response = requests.post(url=url, json=payload)
                response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            return {"error": str(e)}



    def QueryStream(self, query: str, systemprompt: str = None, image_path = None):
        url = f"{self.baseurl}/api/inference"
        payload = {
            "query": query,
            "systemprompt": systemprompt,
            "stream": True
        }
        if self.multimodal and image_path:
            payload = {
                "query": query,
                "systemprompt": systemprompt,
                "image_path" : image_path,
                "stream": False
            }
        else:
            payload = {
                "query": query,
                "systemprompt": systemprompt,
                "stream": False
            }
        try:
            if self.api_key is not None:
                response = requests.post(url=url, headers=self.header, json=payload, stream=True)
            else:
                response = requests.post(url=url, json=payload, stream=True)
            
            if response.status_code == 200:

                for line in response.iter_lines():
                    if line:

                        line = line.decode('utf-8')
                        if line.startswith('data:'):
                            json_str = line[6:]
                            try:
                                chunk_data = json.loads(json_str)
                                chunk = chunk_data.get('chunk', '')
                                sys.stdout.write(chunk)
                                sys.stdout.flush()
                            except json.JSONDecodeError as e:
                                print(f"Error decodificando JSON: {e}")
            else:
                print(f"Error: {response.status_code}")
                try:
                    print(response.json())
                except:
                    print(response.text)
                    
        except requests.RequestException as e:
            return {"error": str(e)}