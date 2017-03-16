from django.http import HttpResponse

class ReturnException():
    def process_exception(self,request,exception):
        return HttpResponse(exception)