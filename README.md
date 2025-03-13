<h1 align="center">AISuperServer</h1>

<div align="center">
  <img src="static/Logo.png" alt="AISuperServer Logo" width="200"/>
</div>

AISuperServer es un servidor de inferencia local potente y fácil de usar, diseñado para ejecutar modelos de IA con Ollama. Proporciona una API REST robusta construida con Flask o FastAPI que permite:

- 🚀 Despliegue rápido de modelos de IA locales
- 🔑 Autenticación configurable mediante API keys
- 📡 Soporte para respuestas en streaming
- 🖼️ Capacidades multimodales para procesamiento de imágenes
- 🛠️ Configuración flexible y monitoreo de recursos

Perfecto para desarrolladores que necesitan una solución ligera y eficiente para servir modelos de IA localmente.

#### Instalación via Pypi

```
pip install AISuperServer
```

## Inicio rápido

### Instalación de Ollama

#### macOS

[Descargar](https://ollama.com/download/Ollama-darwin.zip)

#### Windows

[Descargar](https://ollama.com/download/OllamaSetup.exe)

#### Linux

```shell
curl -fsSL https://ollama.com/install.sh | sh
```

[Instrucciones de instalación manual](https://github.com/ollama/ollama/blob/main/docs/linux.md)

### Descarga del modelo a usar

```
ollama pull <modelo a usar>
```

## Levantar tu servidor

```python
from AISuperServer import SuperServerFlask

app = SuperServerFlask(
    model='deepseek-r1', # Recuerda que aqui vas a usar el modelo que descargaste anteriormente con el Ollama pull
    stream=True,
    port=8080, # Recuerda el puerto donde haz configurado tu servidor para hacer las peticiones
    api_key_required=False,
    enable_memory_monitor=True
)
```

## Levantar tu servidor con FastAPI

```python
from AISuperServer import SuperServerFastAPI

api_keys = ['dummy-apikey-OTXEYCZNS4NBR8YA9V0PBPV4VST2FBAE3PEZDKBDXKCQ88CSTIPI5NPOLN0ZN0CG', 'dummy-apikey-4VQF9L4NFF71GAW4NTOY6EPZUSE6SVNEKW3DHBHWGZIZM8IS8VTT2ZUR75Z0VBZI']

app = SuperServerFastAPI(
    model='qwq:32b', # Recuerda que aqui vas a usar el modelo que descargaste anteriormente con el Ollama pull
    stream=True,
    port=8080, # Recuerda el puerto donde haz configurado tu servidor para hacer las peticiones
    threads=3,
    api_key_required=True, # La opción de API keys ya esta disponible en FastAPI tambien 
    api_keys=api_keys, 
    enable_memory_monitor=True
)
```

Asi de facil es levantar tu servidor de inferencia local con AISuperServer en menos de 20 lineas de código

## Peticiones a tu servidor

### API de health

```python
import requests
import json
import sys

def test_healt():
    x = requests.get('http://0.0.0.0:8080/api/health')
    return x.json()

health = test_healt()
print(health)
```

### API de query a tu modelo

```python
import requests
import json
import sys

def test_query():
    url = 'http://0.0.0.0:8080/api/inference'
    payload = { "query": "Oye haz la función de fibonacci en TypeScript",
                "system_prompt": "Eres un asistente útil y conciso.",
                "stream": False}
    x = requests.post(url, json=payload)
    return x.json()

query = test_query()
print(query)
```

### API de query a tu modelo con respuesta en Stream

```python


import requests
import json
import sys

def test_query_stream():
    url = 'http://0.0.0.0:8080/api/inference'
    payload = {
        "query": "Oye haz la función de fibonacci en TypeScript",
        "system_prompt": "Eres un asistente útil y conciso.",
        "stream" : True
    }
  
    # Usar stream=True en la petición para recibir la respuesta por partes
    response = requests.post(url, json=payload, stream=True)
  
    if response.status_code == 200:
        # Procesar la respuesta SSE línea por línea
        for line in response.iter_lines():
            if line:
                # Las líneas SSE comienzan con "data: "
                line = line.decode('utf-8')
                if line.startswith('data:'):
                    # Extraer el JSON después de "data: "
                    json_str = line[6:]  # Saltamos los primeros 6 caracteres ("data: ")
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

query = test_query_stream()
print(query)

```

# Cliente API de SuperServer

## Cliente API con modelos de Texto

```python
from AISuperServer import SuperServerClient

dummy_api_key = 'dummy-apikey-OTXEYCZNS4NBR8YA9V0PBPV4VST2FBAE3PEZDKBDXKCQ88CSTIPI5NPOLN0ZN0CG'

client = SuperServerClient(api_key=dummy_api_key)
# Toma en cuenta que si tu servidor es levantado en un host y puerto diferente al '0.0.0.0:8080'
# Debes configuraro en el SuperServerClient algo asi: SuperServerClient(host='Tu host', port= 'Tu puerto')
# Y se ha configurado al api_key porque el servidor que levantamos para probar el cliente lo configuramos con api_key
query = client.Query('Oye explicame la secuencia de Fibonacci, como si se lo explicara a un niño pequeño', stream=True)
```

## Cliente API con modelos multimodales

```python
from AISuperServer import SuperServerClient
from pathlib import Path

dummy_api_key = 'dummy-apikey-OTXEYCZNS4NBR8YA9V0PBPV4VST2FBAE3PEZDKBDXKCQ88CSTIPI5NPOLN0ZN0CG'

client = SuperServerClient(api_key=dummy_api_key, multimodal=True)

image_path = Path("Logo.png").resolve()

image_path = str(image_path)

print(image_path)

query = client.Query('Oye describe la imagen y dime que hay de llamativo y de que producto puede ser la imagen', image_path=image_path, stream=True)

# Toma en cuenta que si tu servidor es levantado en un host y puerto diferente al '0.0.0.0:8080'
# Debes configuraro en el SuperServerClient algo asi: SuperServerClient(host='Tu host', port= 'Tu puerto')
# Y se ha configurado al api_key porque el servidor que levantamos para probar el cliente lo configuramos con api_key
```

# Documentación 📚

## Documentación Detallada

En la carpeta [`/tests`](./tests) encontrarás ejemplos completos y documentación detallada sobre:

- 🔧 Configuración avanzada del servidor
- 🔑 Implementación de autenticación con API keys
- 🔄 Manejo de respuestas en streaming
- 🖼️ Procesamiento de imágenes (modo multimodal)
- 📝 Ejemplos prácticos de cada funcionalidad

# Donaciones 💸

Si deseas apoyar este proyecto, puedes hacer una donación a través de PayPal:

[![Donate with PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate?hosted_button_id=KZZ88H2ME98ZG)

Tu donativo permite mantener y expandir nuestros proyectos de código abierto en beneficio de toda la comunidad.
