"""
AISuperServer - Una librería simple para crear servidores de inferencia de IA
"""

__version__ = '0.1.9'

from .localmodel import AILocal
from .create_server import create_inference_serverFlask as SuperServerFlask
from .create_server import create_inference_serverFastAPI as SuperServerFastAPI
from .inferenceapi import InferenceClient as SuperServerClient