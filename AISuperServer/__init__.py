"""
AIServer - Una librería simple para crear servidores de inferencia de IA
"""

__version__ = '0.1.0'

from .localmodel import AILocal
from .server import create_app, ServerConfigModels
from .waitress_server import run_waitress_server
from .create_server import create_inference_server as InferenceServer