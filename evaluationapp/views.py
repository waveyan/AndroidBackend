from django.views.generic.base import View

from androidbackend.settings import ACCESS_TOKEN, MEDIA_ROOT
from userapp.models import User
from hotspotapp.models import HotSpot
from androidbackend.utils import handle_uploaded_file
from .models import Evaluation

from datetime import datetime
import os


class EvaluationBase(View):
    # 获取评论
    def get(self, request):
        pass

    # 发表评论
    def post(self, request):
        access_token = request.POST.get(ACCESS_TOKEN)
        hs_id = request.POST.get('hotspot_id')
        rate = request.POST.get('rate')
        feeling = request.POST.get('feeling')
        price = request.POST.get('price')
        user = User.objects.filter(access_token=access_token).first()
        hotspot = HotSpot.objects.filter(id=hs_id).first()
        i = 0
        for pic in request.FILES.getlist('pic'):
            pic_name = pic.name
            relative_path = str(int(datetime.now().timestamp())) + str(i) + '.' + pic_name.split('.')[-1]
            path = os.path.join(MEDIA_ROOT, 'feeling', user.telephone, relative_path)
            handle_uploaded_file(pic, path)
            i += 1
        evaluation = Evaluation(rate=rate, feeling=feeling, price=price, user=user, hotspot=hotspot)
        evaluation.save()

    # 删除评论
    def delete(self, request):
        pass
