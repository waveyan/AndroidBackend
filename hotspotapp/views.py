from django.views.generic.base import View
from django.http import JsonResponse, QueryDict

from hotspotapp.models import HotSpot, District, Route, City
from userapp.models import User
from androidbackend.utils import message
from androidbackend.settings import ACCESS_TOKEN
from django.views.decorators.http import require_http_methods


class HotSpotBase(View):
    # 获取地点列表,类型待完成！！！
    def get(self, request):
        id = request.GET.get('hotspot_id', '')
        access_token = request.META.get(ACCESS_TOKEN)
        user = User.objects.filter(access_token=access_token).first()
        if id:
            id = int(id)
            hs = HotSpot.objects.filter(id=id).first()
            hs_json = hs.tojson()
            hs_json['activity'] = {'activity': []}
            hs_json['evaluation'] = {'evaluation': []}
            for evaluation in hs.evaluation_set.all():
                hs_json['evaluation']['evaluation'].append(evaluation.tojson_except_hotspot())
            # 活动
            for activity in hs.activity_set.all():
                hs_json['activity']['activity'].append(activity.tojson_except_hotspot())
            for hs in user.favour_hotspot.all():
                if id == hs.id:
                    hs_json['isfavour'] = 1
                    break
            return JsonResponse(hs_json)
        else:
            what = request.GET.get('what')
            city = request.GET.get('cityname')
            if not city:
                city = '广州'
            if what:
                hses=HotSpot.objects.filter(type=what).filter(district__city=city).all()
            else:
                hses=HotSpot.objects.filter(district__city=city).all()
            all_hs_dict = {}
            all_hs_dict['hotspot'] = []
            for item in hses:
                item_json = item.tojson()
                item_json['activity'] = {'activity': []}
                item_json['evaluation'] = {'evaluation': []}
                for hs in user.favour_hotspot.all():
                    if item.id == hs.id:
                        item_json['isfavour'] = 1
                        break
                # # 活动
                for activity in item.activity_set.all():
                    activity_json = activity.tojson_except_hotspot()
                    for a in user.favour_activity.all():
                        if a.id == activity.id:
                            activity_json['isfavour'] = 1
                            break
                    item_json['activity']['activity'].append(activity_json)
                # 评价
                for evaluation in item.evaluation_set.all():
                    item_json['evaluation']['evaluation'].append(evaluation.tojson_except_hotspot())
                all_hs_dict['hotspot'].append(item_json)
            return JsonResponse(all_hs_dict)

    # 推荐地点
    def post(self, request):
        name = request.POST.get('name')
        type = request.POST.get('type')
        address = request.POST.get('address')
        city = request.POST.get('city')
        telephone = request.POST.get('telephone', '')
        worktime = request.POST.get('worktime', '')
        url = request.POST.get('url', '')
        hotspot = HotSpot(name=name, type=type, address=address, city=city, telephone=telephone, worktime=worktime,
                          url=url)
        try:
            hotspot.save()
            msg = message(msg='推荐成功！', status='success')
            return JsonResponse(msg)
        except Exception as e:
            print('推荐地点', e)
            msg = message(msg='推荐失败！')
            return JsonResponse(msg)

    # 点赞
    def put(self, request):
        body = QueryDict(request.body)
        id = body.get('id')
        if id:
            hs = HotSpot.objects.filter(id=id).first()
            if hs:
                try:
                    hs.thumb_up()
                    msg = message(msg='点赞成功！', status='success')
                    return JsonResponse(msg)
                except Exception as e:
                    print('点赞', e)
                    msg = message(msg='点赞失败！')
                    return JsonResponse(msg)
            else:
                msg = message(msg='没有该地点，点赞失败！')
                return JsonResponse(msg)
        else:
            msg = message(msg='信息不全，点赞失败！')
            return JsonResponse(msg)


# 获取城市列表
@require_http_methods(['GET'])
def get_cities(request):
    city = {'city': []}
    for x in City.objects.order_by('-id').all():
        city['city'].append(x.tojson())
    return JsonResponse(city)


# 创建首页
@require_http_methods(['GET'])
def create_index(request):
    user = User.objects.filter(access_token=request.META.get(ACCESS_TOKEN)).first()
    city=request.GET.get('cityname')
    if not city:
        city='广州'
    d = []
    for district in District.objects.filter(city=city).all():
        h = []
        district_json = district.tojson()
        for hs in district.hotspot_set.all():
            hs_json = hs.tojson()
            for f in user.favour_hotspot.all():
                if f.id == hs.id:
                    hs_json['isfavour'] = 1
                    break
            hs_json['activity'] = {'activity': []}
            hs_json['evaluation'] = {'evaluation': []}
            h.append(hs_json)
        district_json['hotspot'] = {'hotspot': h}
        d.append(district_json)
    return JsonResponse({'district': d})


class RouteBase(View):
    # 获取路线
    def get(self, request):
        access_token = request.META.get(ACCESS_TOKEN)
        action = request.GET.get('action')
        route = {'route': []}
        if action == 'person':
            user = User.objects.filter(access_token=access_token).first()
            for r in Route.objects.filter(user=user.telephone).all():
                route['route'].append(r.tojson())
        else:
            for r in Route.objects.all():
                route['route'].append(r.tojson())
        return JsonResponse(route)

    # 提交路线
    def post(self, request):
        title = request.POST.get('title')
        introduce = request.POST.get('introduce')
        time = request.POST.get('time')
        hotspot_ids = request.POST.get('hotspot_ids', '').split(';')
        user = User.objects.filter(access_token=request.META.get(ACCESS_TOKEN)).first()
        route = Route(title=title, introduce=introduce, time=time, user=user.telephone)
        route.save()
        for x in hotspot_ids:
            hs = HotSpot.objects.filter(id=x).first()
            route.hotspot.add(hs)
        msg = message(msg='提交成功！', status='success')
        return JsonResponse(msg)


@require_http_methods(['GET'])
def search(request):
    key = request.GET.get('key', '').replace("'", '').replace('"', '').replace('.', '').replace(';', "")
    user = User.objects.filter(access_token=request.META.get(ACCESS_TOKEN)).first()
    all_hs_dict = {}
    all_hs_dict['hotspot'] = []
    for item in HotSpot.objects.filter(name__contains=key).all():
        item_json = item.tojson()
        item_json['activity'] = {'activity': []}
        item_json['evaluation'] = {'evaluation': []}
        for hs in user.favour_hotspot.all():
            if item.id == hs.id:
                item_json['isfavour'] = 1
                break
        # 活动
        # for activity in item.activity_set.all():
        #     activity_json = activity.tojson_except_hotspot()
        #     for a in user.favour_activity.all():
        #         if a.id == activity.id:
        #             activity_json['isfavour'] = 1
        #             break
        #     item_json['activity']['activity'].append(activity_json)
        # 评价
        # for evaluation in item.evaluation_set.all():
        #     item_json['evaluation']['evaluation'].append(evaluation.tojson_except_hotspot())
        all_hs_dict['hotspot'].append(item_json)
    return JsonResponse(all_hs_dict)
