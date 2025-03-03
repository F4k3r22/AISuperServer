import requests
import json

class Inference:
    def __init__(self, host: str = '0.0.0.0', port: str = '8080'):
        self.baseurl = f"http://{host}:{port}"  # Corregido

    def CheckHealth(self):
        url = f'{self.baseurl}/api/health'
        try:
            response = requests.get(url, timeout=5)  # Agregar timeout
            response.raise_for_status()  # Lanza una excepción si el código de estado no es 200
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def Query(self, query: str, systemprompt: str = None, stream: bool = False):
        url = f"{self.baseurl}/api/inference"
        payload = {
            "query": query,
            "systemprompt": systemprompt,
            "stream": stream
        }

    def QueryStream():
        pass