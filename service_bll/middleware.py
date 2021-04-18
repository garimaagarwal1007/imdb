import encodings

class MiddlewareFacade:
    """Autentication Wrapper confirming to Falcon Middleware Speciifcation"""

    def __init__(self):
        self.logger = None
        self.user_name = 'admin'
        self.password = '123456'

    def process_request(self, req, resp):
        """Process request doc string"""
        pass

    def process_resource(self, req, resp, resource, params):
        """process resource doc string"""
        self.authenticate_admin(req)

    def process_response(self, req, resp, resource, req_succeeded):
        pass

    def authenticate_admin(self, request_parameters):
        user_name = request_parameters.headers['USER']
        password = request_parameters.headers['PASS']
        if self.user_name == user_name and self.password == password:
            request_parameters.context = 'admin'
        else:
            request_parameters.context = 'visitor'
