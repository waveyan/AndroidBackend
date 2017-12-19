from django.views.generic.base import View
from django.http import JsonResponse

from androidbackend.settings import ACCESS_TOKEN, MEDIA_ROOT
from userapp.models import User
from hotspotapp.models import HotSpot
from androidbackend.utils import handle_uploaded_file
from .models import Evaluation
from androidbackend.utils import message

from datetime import datetime
import os


class EvaluationBase(View):
    # 获取评论
    def get(self, request):
        pass

    # 发表评论
    def post(self, request):
        access_token = request.META.get(ACCESS_TOKEN)
        hs_id = request.POST.get('hotspot_id')
        rate = request.POST.get('rate')
        feeling = request.POST.get('feeling')
        price = request.POST.get('price')
        user = User.objects.filter(access_token=access_token).first()
        hotspot = HotSpot.objects.filter(id=hs_id).first()
        i = 0
        for pic in request.FILES.getlist('pic'):
            pic_name = pic.name
            dst_name = str(int(datetime.now().timestamp())) + str(i) + '.' + pic_name.split('.')[-1]
            dst_path = os.path.join(MEDIA_ROOT, 'feeling', user.telephone)
            relative_path = os.path.join('feeling', user.telephone)
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
            dst = os.path.join(dst_path, dst_name)
            handle_uploaded_file(pic, dst)
            i += 1
        evaluation = Evaluation(rate=rate, feeling=feeling, price=price, user=user, hotspot=hotspot, pic=relative_path)
        try:
            evaluation.save()
            msg = message(msg='发表成功！', status='success')
            return JsonResponse(msg)
        except Exception as e:
            print('发表评论', e)
            msg = message(msg='发表失败！')
            return JsonResponse(msg)

    # 删除评论
    def delete(self, request):
        pass
