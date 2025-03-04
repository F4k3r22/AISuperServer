"""
AIServer - Una librería simple para crear servidores de inferencia de IA
"""

__version__ = '0.1.6'

from .localmodel import AILocal
from .create_server import create_inference_server as SuperServer