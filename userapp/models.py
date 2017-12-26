from django.db import models
from django.contrib.auth.models import AbstractUser

from hotspotapp.models import HotSpot
from activityapp.models import Activity


class User(models.Model):
    name = models.CharField("昵称", max_length=50, default='')
    password = models.CharField('密码', max_length=100, default='123456')
    birthday = models.DateField("生日", null=True, blank=True)
    gender = models.CharField("性别", max_length=6, null=True)
    address = models.CharField("地址", max_length=100, default="", null=True)
    telephone = models.CharField("电话", max_length=20, unique=True)
    pic = models.ImageField("头像", default="pic/default.png", max_length=100, null=True)
    introduction = models.CharField("简介", max_length=200, default="", null=True)
    email = models.EmailField("邮箱", max_length=100, unique=True, null=True)
    credit = models.IntegerField('信用值', default=100,null=True)
    access_token = models.CharField('验证头', max_length=100, default='', unique=True,null=True)
    following = models.ManyToManyField('self')
    follower = models.ManyToManyField('self')
    favour_hotspot = models.ManyToManyField(HotSpot)
    favour_activity = models.ManyToManyField(Activity)

    def __str__(self):
        return self.name

    def tojson(self):
        j = {}
        j['name'] = self.name
        j['birthday'] = self.birthday
        j['gender'] = self.gender
        j['address'] = self.address
        j['telephone'] = self.telephone
        j['pic'] = str(self.pic)
        j['introduction'] = self.introduction
        j['email'] = self.email
        j['credit'] = self.credit
        j['evaluation']={'evaluation':[]}
        for x in self.evaluation_set.all():
            j['evaluation']['evaluation'].append(x.tojson_except_user())
        return j


    def tojson_except_evaluation(self):
        j = {}
        j['name'] = self.name
        j['birthday'] = self.birthday
        j['gender'] = self.gender
        j['address'] = self.address
        j['telephone'] = self.telephone
        j['pic'] = str(self.pic)
        j['introduction'] = self.introduction
        j['email'] = self.email
        j['credit'] = self.credit
        return j
