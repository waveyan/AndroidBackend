from django.db import models
from androidbackend.utils import upload_to


class HotSpot(models.Model):
    name = models.CharField("地点名称", max_length=50)
    word = models.CharField("一句话描述", max_length=100, blank=True, null=True)
    worktime = models.CharField("营业时间", max_length=100, null=True)
    price = models.DecimalField("人均消费", max_digits=6, decimal_places=2, null=True)
    city = models.CharField("所在城市", max_length=50, null=True, blank=True)
    pic = models.ImageField("图片", max_length=100, upload_to=upload_to)
    pic1_text = models.CharField('图一解说', max_length=200, default='', null=True)
    pic2_text = models.CharField('图二解说', max_length=200, default='', null=True)
    pic3_text = models.CharField('图三解说', max_length=200, default='', null=True)
    content = models.TextField("内容", max_length=1000)
    address = models.CharField("详细地址", max_length=200)
    url = models.CharField('网址', max_length=200, default='', null=True)
    telephone = models.CharField('联系电话', max_length=30, null=True)
    likes = models.IntegerField("点赞数", default=0)
    type = models.CharField('类型', max_length=50)
    arrived = models.IntegerField('签到数', default=0)

    def __str__(self):
        return self.name

    def tojson(self):
        hs = {}
        hs['id'] = self.id
        hs['name'] = self.name
        hs['word'] = self.word
        hs['worktime'] = self.worktime
        hs['price'] = self.price
        hs['city'] = self.city
        hs['pic'] = str(self.pic)
        hs['pic1_text'] = self.pic1_text
        hs['pic2_text'] = self.pic2_text
        hs['pic3_text'] = self.pic3_text
        hs['content'] = self.content
        hs['address'] = self.address
        hs['like'] = self.likes
        hs['type'] = self.type
        hs['arrived'] = self.arrived
        hs['telephone'] = self.telephone
        hs['url'] = self.url
        return hs

    # def tojson_all(self):
    #     all_hs = []
    #     hs = {}
    #     for item in self.objects.all():
    #         hs['id'] = item.id
    #         hs['name'] = item.name
    #         hs['pic'] = str(item.pic)
    #         all_hs.append(hs)
    #     return all_hs

    def thumb_up(self):
        self.likes += 1
        self.save()
