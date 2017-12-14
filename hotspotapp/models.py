from django.db import models


class HotSpot(models.Model):
    name = models.CharField("城市名称", max_length=50)
    word = models.CharField("一句话描述", max_length=100, blank=True, null=True)
    worktime = models.CharField("营业时间", max_length=100, null=True)
    price = models.DecimalField("人均消费", max_digits=6, decimal_places=2, null=True)
    city = models.CharField("所在城市", max_length=50, null=True, blank=True)
    pic = models.ImageField("图片", max_length=100)
    content = models.CharField("内容", max_length=1000)
    address = models.CharField("详细地址", max_length=200)
    likes = models.IntegerField("点赞数", default=0)
    type = models.CharField('类型', max_length=50)
    arrived = models.IntegerField('签到数', default=0)

    def __str__(self):
        return self.name
