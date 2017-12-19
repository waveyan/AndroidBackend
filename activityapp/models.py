from django.db import models

from hotspotapp.models import HotSpot


# 避免循环引用
# from userapp.models import User


class Activity(models.Model):
    title = models.CharField('活动标题', max_length=100)
    subject = models.CharField('活动主题', max_length=50)
    time = models.DateTimeField('举办时间')
    type = models.CharField('活动类型', max_length=50)
    introduction = models.CharField('活动简介', max_length=200)
    person = models.IntegerField("限定人数", null=True)
    telephone = models.CharField('联系方式', max_length=200)
    website = models.CharField('活动网址', max_length=500)
    pic = models.ImageField('活动图片', max_length=100)
    price = models.DecimalField('费用', max_digits=6, decimal_places=2)
    hotspot = models.ForeignKey(HotSpot, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    host_user = models.CharField('活动发起人账号', max_length=50, null=True)

    def __str__(self):
        return self.title
