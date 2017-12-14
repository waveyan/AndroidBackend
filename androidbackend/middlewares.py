from django.utils.deprecation import MiddlewareMixin
from userapp.models import User
from userapp.utils import message
from django.http import HttpResponse

ignore_url = ['/admin','/login','register/']


class AccessMiddleware(MiddlewareMixin):


    def process_request(self,request):
        print(request.path)
        for url in ignore_url:
            if request.path.startswith(url):
                return None
        access_token = request.META.get('access_token','')
        print(access_token)
        if access_token:
            if User.objects.filter(access_token=access_token).first():
                return None
        msg=message(msg='验证失败！')
        return HttpResponse(msg,content_type='application/json')
