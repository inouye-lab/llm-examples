class GenerativeModel:
    def __init__(self, model_name):
        self.model_name = model_name
    def generate_content(self, prompt):
        class Response:
            def __init__(self, text):
                self.text = text
        return Response("stub")

def configure(api_key=None):
    pass
