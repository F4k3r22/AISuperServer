from AISuperServer import SuperServerFastAPI

app = SuperServerFastAPI(
    model='deepseek-r1', # Recuerda que aqui vas a usar el modelo que descargaste anteriormente con el Ollama pull
    stream=True,
    port=8080, # Recuerda el puerto donde haz configurado tu servidor para hacer las peticiones
    threads=3,
    api_key_required=False, # El uso de API Keys aún no esta implementado en la versión de FastAPI
    enable_memory_monitor=True
)

# Para hacer las request puedes usar los ejemplos en los archivos de testrequest.py tambien con la versión multimodal
# Y hay unos errores raros al hacer peticiones a la API de inferencia desde el Swagger UI