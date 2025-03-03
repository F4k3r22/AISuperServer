from AISuperServer import InferenceServer

#Aún se esta implementando la inferencia de modelos multimodales

app = InferenceServer(
    model='llama3.2-vision',
    stream=True,
    multimodal=True,
    port='8080',
    enable_memory_monitor=True
)

print("Servidor ejecutándose en http://localhost:8080")