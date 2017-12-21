from django.db import models

from hotspotapp.models import HotSpot
from androidbackend.settings import MEDIA_ROOT

import os


def upload_to(instance, filename):
    id = instance.id
    if not id:
        id = Activity.objects.latest('id').id + 1
    return os.path.join('activity', str(id), filename)


class Activity(models.Model):
    title = models.CharField('活动标题', max_length=100)
    subject = models.CharField('活动主题', max_length=50)
    time = models.DateTimeField('举办时间')
    type = models.CharField('活动类型', max_length=50)
    introduction = models.TextField('活动简介', max_length=200)
    person = models.IntegerField("限定人数", null=True, blank=True)
    telephone = models.CharField('联系方式', max_length=200)
    website = models.CharField('活动网址', max_length=500, blank=True)
    pic1 = models.ImageField('活动图片1', upload_to=upload_to,default='activity/default.png', max_length=100, null=True)
    pic3 = models.ImageField('活动图片2', upload_to=upload_to, max_length=100, null=True, blank=True)
    pic2 = models.ImageField('活动图片3', upload_to=upload_to, max_length=100, null=True, blank=True)
    price = models.DecimalField('费用', max_digits=6, decimal_places=2, blank=True)
    hotspot = models.ForeignKey(HotSpot, on_delete=models.CASCADE, null=True,blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    host_user = models.CharField('活动发起人账号', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title

    def tojson(self):
        a = {}
        a['id']=self.id
        a['title'] = self.title
        a['subject'] = self.subject
        a['time'] = self.time
        a['type'] = self.type
        a['introduction'] = self.introduction
        a['person'] = self.person
        a['telephone'] = self.telephone
        a['website'] = self.website
        a['pic1'] = str(self.pic1)
        a['pic2'] = str(self.pic3)
        a['pic3'] = str(self.pic2)
        a['price'] = self.price
        if self.hotspot:
            a['hotspot'] = self.hotspot.tojson()
        return a
