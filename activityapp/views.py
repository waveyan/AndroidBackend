from django.db.utils import IntegrityError
from django.views.generic.base import View
from django.http import JsonResponse, QueryDict
from django.views.decorators.http import require_http_methods

from androidbackend.utils import message, make_security, handle_uploaded_file
from androidbackend.settings import ACCESS_TOKEN, MEDIA_ROOT
from activityapp.models import Activity
from activityapp.forms import ActivityForm
from hotspotapp.models import HotSpot


class ActivityBase(View):

    # 获取活动
    def get(self, request):
        num=request.GET.get('num')
        activities = Activity.objects.all().order_by('id')
        if num:
            activities=activities[:int(num)]
        all_act = {}
        all_act['activity'] = []
        for item in activities:
            all_act['activity'].append(item.tojson())
        return JsonResponse(all_act)

    # 修改活動
    def put(self, request):
        pass

    # 提交活動
    def post(self, request):
        hotspot_id = request.POST.get('hotspot_id')
        activity_form = ActivityForm(request.POST, request.FILES)
        try:
            if activity_form.is_valid():
                if hotspot_id:
                    activity = activity_form.save(commit=False)
                    activity.hotspot = HotSpot.objects.filter(id=hotspot_id).first()
                    activity.save()
                else:
                    activity_form.save()
                msg = message(status='success', msg='创建活动成功')
                return JsonResponse(msg)
        except Exception as e:
            print('提交活动',e)
            msg=message(msg='创建活动失败')
            return JsonResponse(msg)
