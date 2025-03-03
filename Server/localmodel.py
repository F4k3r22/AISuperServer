from ollama import chat, ChatResponse

class AILocal:
    def __init__(self, model, stream=False, format=None):
        self.model = model
        self.stream = stream
        self.format = format

    def query(self, query: str, system_prompt = None):
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
        messages.append({"role": "user", "content": query})
        
        response: ChatResponse = chat(model=self.model, messages=messages, format=self.format)
        return response.message.content
    
    def queryStream(self, query: str, system_prompt = None):
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
        messages.append({"role": "user", "content": query})
        
        stream = chat(model=self.model, messages=messages, stream=True, format=self.format)

        for chunk in stream:
            yield chunk['message']['content']