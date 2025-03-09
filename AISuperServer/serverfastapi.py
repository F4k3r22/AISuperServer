"""
Módulo para crear y configurar la aplicación de FastAPI para el servidor de inferencia
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dataclasses import dataclass
from .localmodel import *
import json

class JSONBodyQueryAPI(BaseModel):
    query: str
    system_prompt: str | None = None
    image_path: str | None = None
    model: str | None = None
    stream: bool = False
    format: str | None = None
    multimodal: bool = False

@dataclass
class ServerConfigModels:
    model: str = None
    stream: bool = None
    format: str = None
    Multimodal: bool = None
    api_key_required: bool = None
    api_keys: list = None

def create_app_FastAPI(config=None):
    """
    Crea y configura una aplicación Flask para inferencia de IA
    
    Args:
        config (ServerConfigModels, optional): Configuración para los modelos
        
    Returns:
        FastAPI: Aplicación de FastAPI configurada
    """

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Todo los origenes
        allow_credentials=True,
        allow_methods=["*"],  # Todos los metodos, e.g., GET, POST, OPTIONS, etc.
        allow_headers=["*"],  # Todos los headers
    )

    app_config = config or ServerConfigModels()

    @app.post('/api/inference')
    async def api(jsonbody: JSONBodyQueryAPI): # Hacia falta poner el async para que Swagger UI pudiera hacer peticiones correctamente
        query = jsonbody.query
        system_prompt = jsonbody.system_prompt
        image_path = jsonbody.image_path
        
        # Obtener configuración del servidor
        server_config = app_config
        
        # Usar modelo de la configuración del servidor si existe, de lo contrario usar el de la petición
        model = server_config.model if server_config.model is not None else jsonbody.model
        
        # Usar stream de la configuración del servidor si existe, de lo contrario usar el de la petición
        stream = server_config.stream if server_config.stream is not None else jsonbody.stream
        
        # Usar format de la configuración del servidor si existe, de lo contrario usar el de la petición
        format = server_config.format if server_config.format is not None else jsonbody.format
        
        Multimodal = server_config.Multimodal if server_config.Multimodal is not None else jsonbody.multimodal

        try:
            Inference = AILocal(model, stream, format, Multimodal)
            if stream:
                def generate():
                    for chunk in Inference.queryStream(query, system_prompt, image_path):
                        yield f"data: {json.dumps({'chunk': chunk})}\n\n"

                return StreamingResponse(generate(), media_type='text/event-stream')
            else:
                return {"response": Inference.query(query, system_prompt, image_path)}
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get('/api/health')
    async def health_check():
        return {
            "status": "ok",
            "config": {
                "model": app_config.model,
                "stream": app_config.stream,
                "format": app_config.format
            }
        }
    
    return app