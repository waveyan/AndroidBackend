from django.views.generic.base import View
from django.http import JsonResponse, QueryDict

from hotspotapp.models import HotSpot
from userapp.models import User
from androidbackend.utils import message
from androidbackend.settings import ACCESS_TOKEN


class HotSpotBase(View):
    # 获取地点列表
    def get(self, request):
        id = request.GET.get('id', '')
        if id:
            id=int(id)
            hs = HotSpot.objects.filter(id=id).first()
            access_token=request.META.get(ACCESS_TOKEN)
            user=User.objects.filter(access_token=access_token).first()
            hs_json=hs.tojson()
            for hs in user.favour_hotspot.all():
                if id == hs.id:
                    hs_json['isfavour']=1
                    break
            return JsonResponse(hs_json)
        else:
            all_hs = []
            for item in HotSpot.objects.all():
                hs = {}
                hs['id'] = item.id
                hs['name'] = item.name
                hs['pic'] = str(item.pic)
                all_hs.append(hs)
            return JsonResponse(all_hs, safe=False)

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
