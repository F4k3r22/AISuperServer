"""
Módulo para crear y configurar la aplicación Flask para el servidor de inferencia
"""

from flask import Flask, request, jsonify, stream_with_context, Response
from flask_cors import CORS
from .localmodel import AILocal
from dataclasses import dataclass
import json

@dataclass
class ServerConfigModels:
    model: str = None
    stream: bool = None
    format: str = None
    Multimodal: bool = None

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
    
    @app.route('/api/inference', methods=['POST'])
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
        format = server_config.format if server_config.format is not None else data.get('format', None)

        Multimodal = server_config.Multimodal if server_config.Multimodal is not None else data.get('multimodal')

        try:
            Inference = AILocal(model, stream, format, Multimodal)
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