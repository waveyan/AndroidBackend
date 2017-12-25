from django.db import models

from hotspotapp.models import HotSpot
from userapp.models import User

from datetime import datetime
import os


def upload_to(instance, filename):
    id = instance.id
    if not id:
        id = Evaluation.objects.latest('id').id + 1
    return os.path.join('feeling', str(id), filename)


class Evaluation(models.Model):
    rate = models.IntegerField('评分', default=0)
    feeling = models.CharField('心情', max_length=200)
    pic1 = models.ImageField('游玩图片', max_length=100, null=True, blank=True, upload_to=upload_to)
    pic2 = models.ImageField('游玩图片', max_length=100, null=True, blank=True, upload_to=upload_to)
    pic3 = models.ImageField('游玩图片', max_length=100, null=True, blank=True, upload_to=upload_to)
    price = models.DecimalField('消费', null=True, max_digits=6, decimal_places=2)
    likes = models.IntegerField('点赞数', default=0)
    hotspot = models.ForeignKey(HotSpot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField('时间', default=datetime.now, null=True, blank=True)

    def __str__(self):
        return self.feeling

    def tojson(self):
        e = {}
        e['rate'] = self.rate
        e['feeling'] = self.feeling
        e['pic1'] = str(self.pic1)
        e['pic2'] = str(self.pic2)
        e['pic3'] = str(self.pic3)
        e['price'] = self.price
        e['likes'] = self.likes
        e['hotspot'] = self.hotspot.tojson()
        e['user'] = self.user.tojson()
        e['time'] = self.time
        return e


class Comment(models.Model):
    word = models.CharField('评论', max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    # comment=models.OneToOneField('self')
    time = models.DateTimeField('时间', default=datetime.now)

    def __str__(self):
        return self.word
