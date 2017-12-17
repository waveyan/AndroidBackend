from django.db.utils import IntegrityError
from django.views.generic.base import View
from django.http import JsonResponse, QueryDict

from userapp.models import User
from androidbackend.utils import message, make_security
from androidbackend.settings import ACCESS_TOKEN, MEDIA_ROOT
# from userapp.forms import UserForm

import os


# class Login(View):
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
# class Register(View):
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
    #
    def get(self, request):
        access_token = request.META.get(ACCESS_TOKEN, '')
        if access_token:
            user = User.objects.filter(access_token=access_token).first()
            return JsonResponse(user.tojson())

    # register and login
    def post(self, request):
        password = request.POST.get('password', '')
        telephone = request.POST.get('telephone', '')
        action = request.POST.get('action', '')
        # if not (password or telephone or action):
        #     msg = message(msg='请求信息不全！')
        #     return JsonResponse(msg)
        # 登陆
        if action == 'login':
            password = make_security(password.encode('utf8'))
            user = User.objects.filter(telephone=telephone, password=password).first()
            if user:
                msg = message(msg='登录成功!', status='success', access_token=user.access_token)
                return JsonResponse(msg)
            else:
                msg = message(msg='账户或密码错误!')
                return JsonResponse(msg)
        # 注册
        elif action == 'register':
            password = make_security(password.encode('utf8'))
            access_token = make_security((telephone + password).encode('utf8'))
            user = User(name=telephone[:2] + telephone[9:], password=password, telephone=telephone,
                        access_token=access_token)
            try:
                user.save()
            except IntegrityError as ie:
                print(ie)
                msg = message(msg='手机重复!')
                return JsonResponse(msg)
            msg = message(msg='注册成功!', status='success')
            return JsonResponse(msg)
        # 修改
        elif action == 'alter':
            access_token = request.META.get(ACCESS_TOKEN, '')
            if access_token:
                user = User.objects.filter(access_token=access_token).first()
                name = request.POST.get('name', '')
                # user_form = UserForm(request.POST, request.FILES, instance=user)
                # if user_form.is_valid():
                #    user_form.save()

                pic = request.FILES.get('pic', '')
                if pic:
                    pic_name = pic.name
                    relative_path = user.telephone + '.' + pic_name.split('.')[-1]
                    path = os.path.join(MEDIA_ROOT, relative_path)
                    handle_uploaded_file(pic, path)
                    user.pic = relative_path
                    user.save()
                if name:
                    user.name = name
                    user.save()
                msg = message(msg='修改成功！', status='success')
                return JsonResponse(msg)
        msg = message(msg='请求信息不全！')
        return JsonResponse(msg)

    # 关注
    def put(self, request):
        follow_id = QueryDict(request.body).get('follow_id')
        access_token = request.META.get(ACCESS_TOKEN, '')
        msg = message(msg='操作失败')
        if access_token and follow_id:
            follow_user = User.objects.filter(pk=follow_id).first()
            user = User.objects.filter(access_token=access_token).first()
            is_following = False
            for x in user.following.all():
                if x.telephone == follow_user.telephone:
                    is_following = True
                    break
            if is_following:
                user.following.remove(follow_user)
                msg = message(msg='取关成功！', status='success')
            else:
                user.following.add(follow_user)
                msg = message(msg='关注成功！', status='success')
        return JsonResponse(msg)


def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
