from ollama import chat, ChatResponse

class AILocal:
    def __init__(self, model, stream=False, format=None, Multimodal=False):
        """
        Inicialiación de la clase de AI Local:
        Args:
            model (str): El modelo a usar
            stream (bool): Por defecto es False es para obtener la repuesta del modelo en Stream
            format (str): Solo se acepta el 'json'
            Multimodal (bool): Por defecto False, toma en cuenta solo es para los modelos de visión y lenguaje
        """
        self.model = model
        self.stream = stream
        self.format = format
        #if self.format != 'json':
        #    raise ValueError('Formato no soportado')
        self.multimodal = Multimodal


    def query(self, query: str, system_prompt = None, image_path = None):
        """
        Realiza una consulta al modelo de Ollama.
        
        Args:
            query (str): La pregunta o prompt para el modelo
            system_prompt (str, optional): Prompt de sistema opcional
            
        Returns:
            str: Respuesta del modelo
        """
        if self.stream:
            return self.queryStream(query, system_prompt)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        user_message = {"role": "user", "content": query}
        if self.multimodal and image_path:
            user_message["images"] = [image_path]
    
        messages.append(user_message)
        
        response: ChatResponse = chat(model=self.model, messages=messages, format=self.format)
        return response.message.content
    
    def queryStream(self, query: str, system_prompt = None, image_path = None):
        """
        Realiza una consulta en modo streaming al modelo de Ollama.
        
        Args:
            query (str): La pregunta o prompt para el modelo
            system_prompt (str, optional): Prompt de sistema opcional
            
        Yields:
            str: Fragmentos de la respuesta del modelo
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        user_message = {"role": "user", "content": query}
        if self.multimodal and image_path:
            user_message["images"] = [image_path]
    
        messages.append(user_message)
        
        stream = chat(model=self.model, messages=messages, stream=True, format=self.format)

        for chunk in stream:
            yield chunk['message']['content']