class MiddlewareMixin:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        response = response or self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # 所有请求都加上允许的url
        response['Access-Control-Allow-Origin'] = '*'
        # 预检请求允许Content-Type Header以及PUT、DELETE方法
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Header'] = 'Content-Type'
            response['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return response
