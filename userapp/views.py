from django.db.utils import IntegrityError
from django.views.generic.base import View
from django.http import HttpResponse
from userapp.models import User

from .utils import message,make_security


class Login(View):
    def post(self,request):
        telephone = request.POST.get("telephone", "")
        password = request.POST.get("password", "")
        if not(telephone or password or telephone):
            msg=message(msg='登录信息不全！')
            return HttpResponse(msg,content_type='application/json')
        password=make_security(password.encode('utf8'))
        user=User.objects.filter(telephone=telephone,password=password).first()
        if user:
            msg = message(msg='登录成功', status='success', access_token=user.access_token)
            return HttpResponse(msg, content_type='application/json')
        else:
            msg = message(msg='账户或密码错误')
            return  HttpResponse(msg, content_type='application/json')


class Register(View):
    def post(self,request):
        name=request.POST.get('name','')
        password=request.POST.get('password','')
        telephone=request.POST.get('telephone','')
        if not(name or password or telephone):
            msg=message(msg='注册信息不全！')
            return HttpResponse(msg,content_type='application/json')
        password=make_security(password.encode('utf8'))
        access_token=make_security((name+password).encode('utf8'))
        user=User(name=name,password=password,telephone=telephone,access_token=access_token)
        try:
            user.save()
        except IntegrityError as ie:
            print(ie)
            msg=message(msg='手机重复')
            return HttpResponse(msg)
        msg=message(msg='注册成功',status='success')
        return HttpResponse(msg,content_type='application/json')



