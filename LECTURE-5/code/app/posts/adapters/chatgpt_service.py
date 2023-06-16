import openai


class HereService:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
    
    def get_response(self, prompt):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return completion.choices[0].message

