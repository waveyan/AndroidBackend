from django.utils.deprecation import MiddlewareMixin
from userapp.models import User
from androidbackend.utils import message
from django.http import JsonResponse
from androidbackend.settings import ACCESS_TOKEN

always_ignore_url = ['/admin', '/media']
ignore_action = ['login', 'register']


class AccessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        for url in always_ignore_url:
            if request.path.startswith(url):
                return None
        action = request.POST.get('action', '')
        if action:
            if action in ignore_action:
                return None
        access_token = request.META.get(ACCESS_TOKEN, '')
        if access_token:
            if User.objects.filter(access_token=access_token).first():
                return None
        msg = message(msg='验证失败！')
        return JsonResponse(msg)
