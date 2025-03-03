"""
Módulo para crear y configurar la aplicación Flask para el servidor de inferencia
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from .localmodel import AILocal
from dataclasses import dataclass

@dataclass
class ServerConfigModels:
    model: str = None
    stream: bool = None
    format: str = None

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
        
        # Obtener configuración del servidor
        server_config = app.config['SERVER_CONFIG']
        
        # Usar modelo de la configuración del servidor si existe, de lo contrario usar el de la petición
        model = server_config.model if server_config.model is not None else data['model']
        
        # Usar stream de la configuración del servidor si existe, de lo contrario usar el de la petición
        stream = server_config.stream if server_config.stream is not None else data.get('stream', False)
        
        # Usar format de la configuración del servidor si existe, de lo contrario usar el de la petición
        format = server_config.format if server_config.format is not None else data.get('format', None)

        try:
            Inference = AILocal(model, stream, format)
            if stream:
                # Cambiado de queryStream a query_stream para seguir convenciones PEP8
                return jsonify({'response': list(Inference.query_stream(query, system_prompt))})
            else:
                return jsonify({'response': Inference.query(query, system_prompt)})
            
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