from django.views.generic.base import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from androidbackend.settings import ACCESS_TOKEN, MEDIA_ROOT
from userapp.models import User
from hotspotapp.models import HotSpot
from androidbackend.utils import handle_uploaded_file
from .models import Evaluation
from .forms import EvaluationForm
from androidbackend.utils import message

from datetime import datetime
import os


class EvaluationBase(View):
    # 获取评论
    def get(self, request):
        access_token = request.META.get(ACCESS_TOKEN)
        action = request.GET.get('action')
        if action == 'person':
            user = User.objects.filter(access_token=access_token).first()
            from collections import defaultdict
            evaluations = defaultdict(lambda: [])
            for x in user.evaluation_set.all():
                evaluations['evaluations'].append(x.tojson())
            return JsonResponse(evaluations)
        else:
            id = request.POST.get('hotspot_id')
            hotspot = HotSpot.objects.filter(id=id).first()
            from collections import defaultdict
            evaluations = defaultdict(lambda: [])
            for x in hotspot.evaluation_set.all():
                evaluations['evaluations'].append(x.tojson())
            return JsonResponse(evaluations)

    # 发表评论
    def post(self, request):
        access_token = request.META.get(ACCESS_TOKEN)
        hotspot_id = request.POST.get('hotspot_id')
        action = request.POST.get('action')
        if action == 'upload_pic':
            evaluation_id = request.POST.get('instance_id')
            evaluation = Evaluation.objects.filter(id=evaluation_id).first()
            evaluation_form = EvaluationForm(request.POST, request.FILES, instance=evaluation)
        else:
            evaluation_form = EvaluationForm(request.POST, request.FILES)
        try:
            if evaluation_form.is_valid():
                evaluation = evaluation_form.save(commit=False)
                evaluation.hotspot = HotSpot.objects.filter(id=hotspot_id).first()
                evaluation.user = User.objects.filter(access_token=access_token).first()
                evaluation.save()
                id = Evaluation.objects.latest('id').id
                msg = message(status='success', msg='发表评论成功！', instance_Id=id)
                return JsonResponse(msg)
            else:
                msg = message(msg='发表评论失败！')
                return JsonResponse(msg)
        except Exception as e:
            print('发表评论', e)
            msg = message(msg='发表评论失败')
            return JsonResponse(msg)

    # 删除评论
    def delete(self, request):
        pass


@require_http_methods(['GET'])
def get_evaluation_from_my_follow(request):
    access_token = request.META.get(ACCESS_TOKEN)
    user = User.objects.filter(access_token=access_token).first()
    evaluation_list = []
    for follow in user.following.all():
        for item in follow.evaluation_set.all():
            evaluation_list.append(item.tojson())
    evaluation_list = sorted(evaluation_list, key=lambda x: x['time'], reverse=True)
    return JsonResponse({'evaluation': evaluation_list})
