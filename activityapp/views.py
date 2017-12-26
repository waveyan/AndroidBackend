from django.views.generic.base import View
from django.http import JsonResponse, QueryDict

from androidbackend.utils import message
from activityapp.models import Activity
from activityapp.forms import ActivityForm
from hotspotapp.models import HotSpot
from userapp.models import User


class ActivityBase(View):

    # 获取活动,action,num
    def get(self, request):
        
        action=request.GET.get('action')
        #活动详情
        if action=='detail':
            act_id=request.GET.get('act_id')
            activity=Activity.objects.filter(id=act_id).first()
            activity_json=activity.tojson()
            host_user=User.objects.filter(telephone=activity.host_user).first()
            if host_user:
                activity_json['host_user']=host_user.tojson()
            return JsonResponse(activity.tojson())
        #获取活动列表,
        else:
            activities=[]
            num = request.GET.get('num')
            activities = Activity.objects.all().order_by('-id')
            if num:
                activities = activities[:int(num)]
            all_act = {}
            all_act['activity'] = []
            for item in activities:
                activity_json=item.tojson()
                host_user=User.objects.filter(telephone=item.host_user).first()
                if host_user:
                    activity_json['host_user']=host_user.tojson()
                all_act['activity'].append(activity_json)
            return JsonResponse(all_act)



    # 修改活動
    def put(self, request):
        pass

    # 提交活動
    def post(self, request):
        hotspot_id = request.POST.get('hotspot_id')
        activity_id = request.POST.get('instance_id')
        action = request.POST.get('action')
        if action == 'upload_pic':
            activity = Activity.objects.filter(id=activity_id).first()
            activity_form = ActivityForm(request.POST, request.FILES, instance=activity)
        else:
            activity_form = ActivityForm(request.POST, request.FILES)
        try:
            if activity_form.is_valid():
                if hotspot_id:
                    activity = activity_form.save(commit=False)
                    activity.hotspot = HotSpot.objects.filter(id=hotspot_id).first()
                    activity.save()
                else:
                    activity_form.save()
                id = Activity.objects.latest('id').id
                msg = message(status='success', msg='操作活动成功', instance_Id=id)
                return JsonResponse(msg)
            else:
                msg = message(msg='操作活动失败')
                return JsonResponse(msg)
        except Exception as e:
            print('操作活动', e)
            msg = message(msg='操作活动失败')
            return JsonResponse(msg)
