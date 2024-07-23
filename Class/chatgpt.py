from openai import OpenAI
import os

class ChatGPT:  
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_APIKEY', None))
        self.model = os.getenv("OPENAI_MODEL", None)
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", None))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", None))

    def get_response(self, message):
        prompt = message[4:]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        reply_msg = response.choices[0].message.content.strip()
        print('AI回答內容' + reply_msg)
        return reply_msg
