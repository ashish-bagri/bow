class APIAutheticate:
    def __init__(self, config):
        self.api_authentication = config['authentication'].lower() == 'true'
        self.api_username = None
        self.api_password = None
        if self.api_authentication:
            self.api_username = config['user']
            self.api_password = config['password']
            self.api_username_header = config['user_header']
            self.api_password_header = config['password_header']

    def authenticate(self, headers):
        if not self.api_authentication:
            return True
        else:
            if self.api_username_header in headers and self.api_password_header in headers:
                return headers[self.api_username_header] == self.api_username \
                       and headers[self.api_password_header] == self.api_password

        return False
