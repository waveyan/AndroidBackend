from django.views.generic.base import View
from django.http import JsonResponse, QueryDict
from django.views.decorators.http import require_http_methods

from androidbackend.settings import ACCESS_TOKEN, MEDIA_ROOT
from userapp.models import User
from hotspotapp.models import HotSpot
from .models import Evaluation
from .forms import EvaluationForm
from androidbackend.utils import message


class EvaluationBase(View):
    # 获取评论
    def get(self, request):
        access_token = request.META.get(ACCESS_TOKEN)
        action = request.GET.get('action')
        if action == 'person':
            user_tel = request.GET.get('user_tel')
            if user_tel:
                user = User.objects.filter(telephone=user_tel).first()
            else:
                user = User.objects.filter(access_token=access_token).first()
            from collections import defaultdict
            evaluations = defaultdict(lambda: [])
            for x in user.evaluation_set.order_by('-time').all():
                evaluations['evaluation'].append(x.tojson())
            return JsonResponse(evaluations)
        elif action == 'hotspot':
            hotspot_id = request.GET.get('hotspot_id')
            hotspot = HotSpot.objects.filter(id=hotspot_id).first()
            from collections import defaultdict
            evaluations = defaultdict(lambda: [])
            for x in hotspot.evaluation_set.all():
                evaluations['evaluation'].append(x.tojson())
            return JsonResponse(evaluations)
        else:
            id = request.POST.get('hotspot_id')
            hotspot = HotSpot.objects.filter(id=id).first()
            from collections import defaultdict
            evaluations = defaultdict(lambda: [])
            for x in hotspot.evaluation_set.all():
                evaluations['evaluation'].append(x.tojson())
            return JsonResponse(evaluations)

    # 发表评论
    def post(self, request):
        access_token = request.META.get(ACCESS_TOKEN)
        hotspot_id = request.POST.get('hotspot_id')
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

    # 点赞
    def put(self, request):
        body = QueryDict(request.body)
        user = User.objects.filter(access_token=request.META.get(ACCESS_TOKEN)).first()
        evaluation_id = body.get('evaluation_id')
        evaluation = Evaluation.objects.filter(pk=evaluation_id).first()
        islike = True
        for usr in evaluation.usr_like.all():
            if usr.id == user.id:
                islike = False
                break
        if islike:
            evaluation.usr_like.add(user)
            msg = message(status='success_like', msg='点赞成功')
        else:
            evaluation.usr_like.remove(user)
            msg = message(status='success_unlike', msg='取消点赞')
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
    for x in user.evaluation_set.all():
        evaluation_list.append(x.tojson())
    evaluation_list = sorted(evaluation_list, key=lambda x: x['time'], reverse=True)
    return JsonResponse({'evaluation': evaluation_list})
