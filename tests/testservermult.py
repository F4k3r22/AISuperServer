from AISuperServer import SuperServer

#Aún se esta implementando la inferencia de modelos multimodales

app = SuperServer(
    model='llama3.2-vision',
    stream=True,
    multimodal=True,
    port='8080',
    enable_memory_monitor=True
)

print("Servidor ejecutándose en http://localhost:8080")