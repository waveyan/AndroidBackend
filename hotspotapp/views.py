from django.views.generic.base import View
from django.http import JsonResponse, QueryDict

from hotspotapp.models import HotSpot
from androidbackend.utils import message

class HotSpotBase(View):
    # 获取地点列表
    def get(self, request):
        id = request.GET.get('id', '')
        if id:
            hs = HotSpot.objects.filter(id=id).first()
            return JsonResponse(hs.tojson())
        else:
            all_hs = []
            for item in HotSpot.objects.all():
                hs = {}
                hs['id'] = item.id
                hs['name'] = item.name
                hs['pic'] = str(item.pic)
                all_hs.append(hs)
            return JsonResponse(all_hs, safe=False)

    # 点赞
    def put(self, request):
        body = QueryDict(request.body)
        id = body.get('id')
        if id:
            hs = HotSpot.objects.filter(id=id).first()
            if hs:
                try:
                    hs.thumb_up()
                    msg=message(msg='点赞成功！',status='success')
                    return JsonResponse(msg)
                except Exception as e:
                    print('点赞',e)
                    msg = message(msg='点赞失败！')
                    return JsonResponse(msg)
            else:
                msg = message(msg='没有该地点，点赞失败！')
                return JsonResponse(msg)
        else:
            msg = message(msg='信息不全，点赞失败！')
            return JsonResponse(msg)
