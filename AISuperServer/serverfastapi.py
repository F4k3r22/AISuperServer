"""
Módulo para crear y configurar la aplicación de FastAPI para el servidor de inferencia
"""
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Optional, List, Callable, Any
from .localmodel import *
import json
from functools import wraps

class JSONBodyQueryAPI(BaseModel):
    query: str
    system_prompt: Optional[str] = None
    image_path: Optional[str] = None
    model: Optional[str] = None
    stream: bool = False
    format: Optional[str] = None
    multimodal: bool = False

@dataclass
class ServerConfigModels:
    model: Optional[str] = None
    stream: Optional[bool] = None
    format_response: Optional[str] = None
    Multimodal: Optional[bool] = None
    api_key_required: Optional[bool] = None
    api_keys: Optional[List[str]] = None

def create_app_FastAPI(config=None):
    """
    Crea y configura una aplicación FastAPI para inferencia de IA
    
    Args:
        config (ServerConfigModels, optional): Configuración para los modelos
        
    Returns:
        FastAPI: Aplicación de FastAPI configurada
    """

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app_config = config or ServerConfigModels()
    
    # Dependencia para verificar API key
    async def require_api_key(x_api_key: str = Header(None)):
        """
        Dependencia que verifica si la API key proporcionada es válida
        
        Args:
            x_api_key (str): API key proporcionada en el header X-API-Key
            
        Raises:
            HTTPException: Si la API key no es proporcionada o no es válida
            
        Returns:
            str: La API key si es válida
        """
        if not x_api_key:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "API Key missing",
                    "message": "X-API-Key header is required"
                }
            )
            
        if not app_config.api_keys or not isinstance(app_config.api_keys, list):
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Invalid server configuration",
                    "message": "API keys are not properly configured"
                }
            )
            
        if x_api_key not in app_config.api_keys:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Invalid API Key",
                    "message": "The provided API key is not valid"
                }
            )
            
        return x_api_key
    
    # Dependencia condicional para la API key
    async def conditional_require_api_key(x_api_key: str = Header(None)):
        """
        Dependencia que verifica la API key solo si está configurado así en el servidor
        
        Args:
            x_api_key (str): API key proporcionada en el header X-API-Key
            
        Returns:
            str: La API key si es válida o None si no se requiere
        """
        if app_config.api_key_required:
            return await require_api_key(x_api_key)
        return None
    
    @app.post('/api/inference')
    async def api(
        jsonbody: JSONBodyQueryAPI,
        api_key: str = Depends(conditional_require_api_key)
    ):
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
        format_response = server_config.format_response if server_config.format_response is not None else jsonbody.format
        
        Multimodal = server_config.Multimodal if server_config.Multimodal is not None else jsonbody.multimodal
        
        try:
            Inference = AILocal(model, stream, format_response, Multimodal)
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
    async def health_check(api_key: str = Depends(conditional_require_api_key)):
        return {
            "status": "ok",
            "config": {
                "model": app_config.model,
                "stream": app_config.stream,
                "format": app_config.format_response
            }
        }
    
    return app