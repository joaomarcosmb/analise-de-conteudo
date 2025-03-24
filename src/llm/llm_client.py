from openai import OpenAI


class LLMClient:
    def __init__(self, endpoint_url):
        self.client = OpenAI(
            base_url=endpoint_url,
            api_key='ollama'
        )

    def generate(self, prompt, model='gemma3', temperature=0.7, top_p=1):
        """Gera uma resposta textual usando um LLM"""
        messages = [
            {
                'role': 'system',
                'content': 'Você é um assistente de IA que responde perguntas e ajuda com tarefas.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                top_p=top_p
            )

            if response.choices[0].message.content:
                return response.choices[0].message.content
            else:
                return None

        except Exception as e:
            print(f'Erro ao chamar LLM: {e}')
