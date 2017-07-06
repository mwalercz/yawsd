class Authentication:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_headers(self):
        return {
            'x-api-key': self.api_key
        }
