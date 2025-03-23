from .localmodel import *
from .server import *
from .waitress_server import *
from .uvicorn_server import *
from .serverfastapi import *
import asyncio

# Función principal para iniciar un servidor completo
def create_inference_serverFlask(
    model=None, 
    stream=None, 
    format_response=None,
    multimodal=None, 
    host='0.0.0.0', 
    port=8080,
    api_key_required: bool = None,
    api_keys: list = None,
    parallel_requests: Optional[str] = "4",
    threads=5,
    enable_memory_monitor=True
):
    """
    Crea y ejecuta un servidor de inferencia de IA completo.
    
    Args:
        model (str, optional): Modelo por defecto a utilizar
        stream (bool, optional): Si se debe usar streaming por defecto
        format_response (str, optional): Formato de salida por defecto
        host (str): Host para el servidor
        port (int): Puerto para el servidor
        api_key_required (bool): Activar si quieres que tu API requiera de API Keys para hacer peticiones
        api_keys (list): Lista de las API keys validas (Aún en mejora)
        threads (int): Número de hilos para Waitress
        enable_memory_monitor (bool): Activar monitoreo de memoria
        
    Returns:
        flask.Flask: La aplicación Flask creada
    """
    # Configurar valores por defecto
    config = ServerConfigModels(
        model=model,
        stream=stream,
        format_response=format_response,
        Multimodal=multimodal,
        api_key_required=api_key_required,
        api_keys=api_keys,
        parallel_requests=parallel_requests
    )
    
    # Crear la aplicación
    app = create_app(config)
    
    # Ejecutar con Waitress en un hilo separado
    run_waitress_server(
        app, 
        host=host, 
        port=port, 
        threads=threads,
        enable_memory_monitor=enable_memory_monitor
    )
    
    return app

def create_inference_serverFastAPI(
    model=None, 
    stream=None, 
    format_response=None,
    multimodal=None, 
    host='0.0.0.0', 
    port=8080,
    api_key_required: bool = None,
    api_keys: list = None,
    parallel_requests: Optional[str] = "4",
    threads=5,
    enable_memory_monitor=True
):
    """
    Crea y ejecuta un servidor de inferencia de IA completo.
    
    Args:
        model (str, optional): Modelo por defecto a utilizar
        stream (bool, optional): Si se debe usar streaming por defecto
        format_response (str, optional): Formato de salida por defecto
        host (str): Host para el servidor
        port (int): Puerto para el servidor
        api_key_required (bool): Activar si quieres que tu API requiera de API Keys para hacer peticiones
        api_keys (list): Lista de las API keys validas (Aún en mejora)
        threads (int): Número de hilos para Waitress
        enable_memory_monitor (bool): Activar monitoreo de memoria
        
    Returns:
        fastapi.FastAPI: La aplicación FastAPI creada
    """
    # Configurar valores por defecto
    config = ServerConfigModels(
        model=model,
        stream=stream,
        format_response=format_response,
        Multimodal=multimodal,
        api_key_required=api_key_required,
        api_keys=api_keys,
        parallel_requests=parallel_requests
    )
    
    # Crear la aplicación
    app = create_app_FastAPI(config)
    
    
    asyncio.run(run_uvicorn_server(
        app, 
        host=host, 
        port=port, 
        workers=threads,
        enable_memory_monitor=enable_memory_monitor
    ))
    
    return app