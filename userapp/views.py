from django.db.utils import IntegrityError
from django.views.generic.base import View
from django.http import JsonResponse,QueryDict
from userapp.models import User

from androidbackend.utils import message,make_security


#class Login(View):
#    def post(self,request):
#        telephone = request.POST.get("telephone", "")
#        password = request.POST.get("password", "")
#        if not(telephone or password or telephone):
#            msg=message(msg='登录信息不全！')
#            return JsonResponse(msg,content_type='application/json')
#        password=make_security(password.encode('utf8'))
#        user=User.objects.filter(telephone=telephone,password=password).first()
#        if user:
#            msg = message(msg='登录成功', status='success', access_token=user.access_token)
#            return JsonResponse(msg, content_type='application/json')
#        else:
#            msg = message(msg='账户或密码错误')
#            return  JsonResponse(msg, content_type='application/json')
#
#
#class Register(View):
#    def post(self,request):
#        name=request.POST.get('name','')
#        password=request.POST.get('password','')
#        telephone=request.POST.get('telephone','')
#        if not(name or password or telephone):
#            msg=message(msg='注册信息不全！')
#            return JsonResponse(msg,content_type='application/json')
#        password=make_security(password.encode('utf8'))
#        access_token=make_security((name+password).encode('utf8'))
#        user=User(name=name,password=password,telephone=telephone,access_token=access_token)
#        try:
#            user.save()
#        except IntegrityError as ie:
#            print(ie)
#            msg=message(msg='手机重复')
#            return JsonResponse(msg)
#        msg=message(msg='注册成功',status='success')
#        return JsonResponse(msg,content_type='application/json')

class UserManager(View):
    def get(self,request):
        telephone = request.GET.get("telephone", "")
        password = request.GET.get("password", "")
        if not(telephone or password or telephone):
            msg=message(msg='登录信息不全！')
            return JsonResponse(msg)
        password=make_security(password.encode('utf8'))
        user=User.objects.filter(telephone=telephone,password=password).first()
        if user:
            msg = message(msg='登录成功', status='success', access_token=user.access_token)
            return JsonResponse(msg)
        else:
            msg = message(msg='账户或密码错误')
            return  JsonResponse(msg)
    
    def post(self,request):
        password=request.POST.get('password','')
        telephone=request.POST.get('telephone','')
        if not( password or telephone):
            msg=message(msg='注册信息不全！')
            return JsonResponse(msg)
        password=make_security(password.encode('utf8'))
        access_token=make_security((telephone+password).encode('utf8'))
        user=User(password=password,telephone=telephone,access_token=access_token)
        try:
            user.save()
        except IntegrityError as ie:
            print(ie)
            msg=message(msg='手机重复')
            return JsonResponse(msg)
        msg=message(msg='注册成功',status='success')
        return JsonResponse(msg)

    def put(self,request):
        body=QueryDict(request.body,encoding=request.encoding)
        msg={'msg':body.get('telephone')}
        return JsonResponse(msg)

    def delete(self,request):
        print(request.body)
        body=QueryDict(request.body,encoding=request.encoding)
        user=User.objects.filter(telephone=body.get('telephone')).first()
        return JsonResponse({'user':user.toJSON()})


