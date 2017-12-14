from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    name = models.CharField("昵称", max_length=50, default='')
    password = models.CharField('密码', max_length=100, default='123456')
    birday = models.DateField("生日", null=True, blank=True)
    gender = models.CharField("性别", max_length=6, null=True)
    address = models.CharField("地址", max_length=100, default="", null=True)
    telephone = models.CharField("电话", max_length=20, unique=True)
    pic = models.ImageField("头像", upload_to="image/%Y/%m", default="image/default.png", max_length=100, null=True)
    introduction = models.CharField("简介", max_length=200, default="", null=True)
    email = models.EmailField("邮箱", max_length=100, unique=True, null=True)
    credit = models.IntegerField('信用值', default=100)
    access_token = models.CharField('验证头', max_length=100, default='', unique=True)
    following = models.ManyToManyField('self')
    follower = models.ManyToManyField('self')

    def __str__(self):
        return self.name
