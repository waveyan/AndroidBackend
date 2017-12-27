from django.db.utils import IntegrityError
from django.views.generic.base import View
from django.http import JsonResponse, QueryDict
from django.views.decorators.http import require_http_methods

from userapp.models import User
from androidbackend.utils import message, make_security, handle_uploaded_file
from androidbackend.settings import ACCESS_TOKEN, MEDIA_ROOT
# from userapp.forms import UserForm
from hotspotapp.models import HotSpot
from activityapp.models import Activity

import os


class UserManager(View):
    # detail
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
                    dst_name = user.telephone + '.' + pic_name.split('.')[-1]
                    dst_path = os.path.join(MEDIA_ROOT, 'pic')
                    dst = os.path.join(dst_path, dst_name)
                    relative_path = os.path.join('pic', dst_name)
                    handle_uploaded_file(pic, dst)
                    user.pic = relative_path
                    user.save()
                if name:
                    user.name = name
                    user.save()
                msg = message(msg='修改成功！', status='success')
                return JsonResponse(msg)
        msg = message(msg='请求信息不全！')
        return JsonResponse(msg)

    # 关注 and 收藏
    def put(self, request):
        body = QueryDict(request.body)
        msg = message(msg='操作失败！')
        action = body.get('action')
        access_token = request.META.get(ACCESS_TOKEN, '')
        # 关注好友
        if action == 'follow':
            follow_id = body.get('follow_id')
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
                    msg = message(msg='取关成功！', status='success_unfollow')
                else:
                    user.following.add(follow_user)
                    msg = message(msg='关注成功！', status='success_follow')
        # 收藏地点
        elif action == 'favour_hs':
            hs_id = body.get('hotspot_id')
            if hs_id:
                hs_id = int(hs_id)
                hotspot = HotSpot.objects.filter(id=hs_id).first()
                user = User.objects.filter(access_token=access_token).first()
                is_favour = False
                for x in user.favour_hotspot.all():
                    if x.id == hs_id:
                        is_favour = True
                        break
                if is_favour:
                    user.favour_hotspot.remove(hotspot)
                    msg = message(msg='取消收藏成功！', status='success_unfavour')
                else:
                    user.favour_hotspot.add(hotspot)
                    msg = message(msg='收藏成功！', status='success_favour')
        # 收藏活动
        elif action == 'favour_act':
            act_id = body.get('activity_id')
            if act_id:
                act_id = int(act_id)
                activity = Activity.objects.filter(id=act_id).first()
                user = User.objects.filter(access_token=access_token).first()
                is_favour = False
                for x in user.favour_activity.all():
                    if x.id == act_id:
                        is_favour = True
                        break
                if is_favour:
                    user.favour_activity.remove(activity)
                    msg = message(msg='取消收藏成功！', status='success_unfavour')
                else:
                    user.favour_activity.add(activity)
                    msg = message(msg='收藏成功！', status='success_favour')
        return JsonResponse(msg)


# 粉丝和关注列表
@require_http_methods(['GET'])
def get_my_follow(request):
    access_token = request.META.get(ACCESS_TOKEN)
    user = User.objects.filter(access_token=access_token).first()
    from collections import defaultdict
    follow = defaultdict(lambda: [])
    for fans in user.following.all():
        follow['following'].append(fans.tojson())
    for follower in user.follower.all():
        follow['follower'].append(follower.tojson())
    return JsonResponse(follow)


# 收藏列表
@require_http_methods(['GET'])
def get_my_favour(request):
    access_token = request.META.get(ACCESS_TOKEN)
    user = User.objects.filter(access_token=access_token).first()
    from collections import defaultdict
    favour = defaultdict(lambda: [])
    for hs in user.favour_hotspot.all():
        hs_json = hs.tojson()
        hs_json['isfavour'] = 1
        favour['hotspot'].append(hs_json)
    # 注意！！
    for activity in user.favour_activity.all():
        activity_json = activity.tojson()
        host_user = User.objects.filter(telephone=activity.host_user).first()
        if host_user:
            activity_json['host_user'] = host_user.tojson()
        activity_json['isfavour'] = 1
        favour['activity'].append(activity_json)
    # 可能有路线
    return JsonResponse(favour)


# 我创建的活动
@require_http_methods(['GET'])
def get_my_activity(request):
    access_token = request.META.get(ACCESS_TOKEN)
    user = User.objects.filter(access_token=access_token).first()
    my_activities = Activity.objects.filter(host_user=user.telephone).all()
    my_act = {'activity': []}
    for a in my_activities:
        activity_json = a.tojson()
        for item in user.favour_activity.all():
            if a.id==item.id:
                activity_json['isfavour']=1
                break
        activity_json['host_user'] = user.tojson()
        my_act['activity'].append(activity_json)
    return JsonResponse(my_act)
