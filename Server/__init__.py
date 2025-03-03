"""
AIServer - Una librería simple para crear servidores de inferencia de IA
"""

__version__ = '0.1.0'

from .localmodel import AILocal
from .server import create_app, ServerConfigModels
from .waitress_server import run_waitress_server

# Función principal para iniciar un servidor completo
def create_inference_server(
    model=None, 
    stream=None, 
    format=None, 
    host='0.0.0.0', 
    port=8080, 
    threads=5,
    enable_memory_monitor=True
):
    """
    Crea y ejecuta un servidor de inferencia de IA completo.
    
    Args:
        model (str, optional): Modelo por defecto a utilizar
        stream (bool, optional): Si se debe usar streaming por defecto
        format (str, optional): Formato de salida por defecto
        host (str): Host para el servidor
        port (int): Puerto para el servidor
        threads (int): Número de hilos para Waitress
        enable_memory_monitor (bool): Activar monitoreo de memoria
        
    Returns:
        flask.Flask: La aplicación Flask creada
    """
    # Configurar valores por defecto
    config = ServerConfigModels(
        model=model,
        stream=stream,
        format=format
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