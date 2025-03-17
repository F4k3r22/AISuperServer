"""
Módulo para crear y configurar la aplicación Flask para el servidor de inferencia
"""

from flask import Flask, request, jsonify, stream_with_context, Response
from flask_cors import CORS
from .localmodel import AILocal
from dataclasses import dataclass
import json
from functools import wraps
from typing import Callable, Any

@dataclass
class ServerConfigModels:
    model: str = None
    stream: bool = None
    format_response: str = None
    Multimodal: bool = None
    api_key_required: bool = None
    api_keys: list = None

def create_app(config=None):
    """
    Crea y configura una aplicación Flask para inferencia de IA
    
    Args:
        config (ServerConfigModels, optional): Configuración para los modelos
        
    Returns:
        Flask: Aplicación Flask configurada
    """
    app = Flask(__name__)
    CORS(app)
    
    # Configuración global para los modelos
    app.config['SERVER_CONFIG'] = config or ServerConfigModels()

    def require_api_key(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any) -> Any:
            server_config = app.config.get('SERVER_CONFIG')
            
            if not server_config:
                return jsonify({
                    "error": "Server configuration missing",
                    "message": "Server is not properly configured"
                }), 500

            provided_key = request.headers.get('X-API-Key')
            
            if not provided_key:
                return jsonify({
                    "error": "API Key missing",
                    "message": "X-API-Key header is required"
                }), 401

            if not server_config.api_keys or not isinstance(server_config.api_keys, list):
                return jsonify({
                    "error": "Invalid server configuration",
                    "message": "API keys are not properly configured"
                }), 500

            if provided_key not in server_config.api_keys:
                return jsonify({
                    "error": "Invalid API Key",
                    "message": "The provided API key is not valid"
                }), 403

            return f(*args, **kwargs)
        return decorated_function

    def conditional_require_api_key(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            server_config = app.config.get('SERVER_CONFIG')
            
            if not server_config:
                return f(*args, **kwargs)

            if server_config.api_key_required:
                return require_api_key(f)(*args, **kwargs)
            
            return f(*args, **kwargs)
        return wrapper
    
    @app.route('/api/inference', methods=['POST'])
    @conditional_require_api_key
    def api():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        query = data['query']
        system_prompt = data['system_prompt'] if 'system_prompt' in data else None
        image_path = data['image_path'] if 'image_path' in data else None
        
        # Obtener configuración del servidor
        server_config = app.config['SERVER_CONFIG']
        
        # Usar modelo de la configuración del servidor si existe, de lo contrario usar el de la petición
        model = server_config.model if server_config.model is not None else data['model']
        
        # Usar stream de la configuración del servidor si existe, de lo contrario usar el de la petición
        stream = server_config.stream if server_config.stream is not None else data.get('stream', False)
        
        # Usar format de la configuración del servidor si existe, de lo contrario usar el de la petición
        format_response = server_config.format if server_config.format_response is not None else data.get('format', None)

        Multimodal = server_config.Multimodal if server_config.Multimodal is not None else data.get('multimodal')

        try:
            Inference = AILocal(model, stream, format_response, Multimodal)
            if stream:
                def generate():
                    for chunk in Inference.queryStream(query, system_prompt, image_path):
                        yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        
                return Response(stream_with_context(generate()), 
                                mimetype='text/event-stream')

            else:
                return jsonify({'response': Inference.query(query, system_prompt, image_path)})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Endpoint para verificar estado del servidor
    @app.route('/api/health', methods=['GET'])
    @conditional_require_api_key
    def health_check():
        return jsonify({
            'status': 'ok',
            'config': {
                'model': app.config['SERVER_CONFIG'].model,
                'stream': app.config['SERVER_CONFIG'].stream,
                'format': app.config['SERVER_CONFIG'].format
            }
        })
    
    return app

# Para ejecutar directamente este archivo (para pruebas)
#if __name__ == '__main__':
#    app = create_app()
#    app.run(host='0.0.0.0', debug=True)