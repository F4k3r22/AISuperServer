from AISuperServer import SuperServerFlask

app = SuperServerFlask(
    model='llama3.2-vision',
    stream=True,
    multimodal=True,
    port=8080,
    api_key_required=False,
    enable_memory_monitor=True
)

print("Servidor ejecutándose en http://0.0.0.0:8080")