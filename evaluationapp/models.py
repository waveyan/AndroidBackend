from django.db import models

from hotspotapp.models import HotSpot
from userapp.models import User

from datetime import datetime


class Evaluation(models.Model):
    rate = models.IntegerField('评分', default=0)
    feeling = models.CharField('心情', max_length=200)
    pic = models.ImageField('游玩图片', max_length=100, null=True)
    price = models.DecimalField('消费', null=True, max_digits=6, decimal_places=2)
    likes = models.IntegerField('点赞数', default=0)
    hotspot = models.ForeignKey(HotSpot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField('时间', default=datetime.now)

    def __str__(self):
        return self.feeling


class Comment(models.Model):
    word = models.CharField('评论', max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    # comment=models.OneToOneField('self')
    time = models.DateTimeField('时间', default=datetime.now)

    def __str__(self):
        return self.word
