from django.db import models

import os


def upload_to(instance, filename):
    id = instance.id
    if not instance:
        id = HotSpot.objects.latest('id').id + 1
    return os.path.join('hotspot', str(id), filename)


def d_upload_to(instance, filename):
    id = instance.id
    if not instance:
        id = HotSpot.objects.latest('id').id + 1
    return os.path.join('district', str(id), filename)


def c_upload_to(instance, filename):
    # id = instance.id
    # if not instance:
    #     id = HotSpot.objects.latest('id').id + 1
    return os.path.join('city', filename)


class City(models.Model):
    englishname=models.CharField("英文名称",max_length=100,null=True)
    name = models.CharField('城市名称', max_length=50)
    pic = models.ImageField('图片', upload_to=c_upload_to)

    def __str__(self):
        return self.name

    def tojson(self):
        c = {}
        c['id']=self.id
        c['englishname']=self.englishname
        c['name'] = self.name
        c['pic'] = str(self.pic)
        return c


class District(models.Model):
    name = models.CharField("区域", max_length=50)
    englishName = models.CharField('英文名字', max_length=100)
    city = models.CharField("所在城市", max_length=50)
    city_obj = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    introduction = models.TextField('介绍', max_length=500)
    pic = models.ImageField('图片', max_length=50, upload_to=d_upload_to)
    longitude = models.CharField('经度', max_length=20, null=True)
    latitude = models.CharField('纬度', max_length=20, null=True)

    def tojson(self):
        d = {}
        d['name'] = self.name
        d['englishname'] = self.englishName
        d['city'] = self.city
        d['introduction'] = self.introduction
        d['pic'] = str(self.pic)
        d['hotspot'] = {'hotspot': []}
        d['longitude'] = self.longitude
        d['latitude'] = self.latitude
        return d

    def __str__(self):
        return self.name


class HotSpot(models.Model):
    name = models.CharField("地点名称", max_length=50)
    englishname = models.CharField("英文名称", max_length=100, null=True)
    word = models.CharField("一句话描述", max_length=100, blank=True, null=True)
    worktime = models.CharField("营业时间", max_length=100, null=True)
    price = models.CharField("人均消费", max_length=30, null=True)
    pic1 = models.ImageField("图片一", max_length=100, upload_to=upload_to, default='')
    pic1_text = models.CharField('图一解说', max_length=200, default='', null=True)
    pic2 = models.ImageField("图二", max_length=100, upload_to=upload_to, default='')
    pic2_text = models.CharField('图二解说', max_length=200, default='', null=True)
    pic3 = models.ImageField("图片三", max_length=100, upload_to=upload_to, default='')
    pic3_text = models.CharField('图三解说', max_length=200, default='', null=True)
    content = models.TextField("内容", max_length=1000)
    address = models.CharField("详细地址", max_length=200)
    url = models.CharField('网址', max_length=200, default='', null=True)
    telephone = models.CharField('联系电话', max_length=30, null=True)
    likes = models.IntegerField("点赞数", default=0)
    type = models.CharField('类型', max_length=50)
    arrived = models.IntegerField('签到数', default=0)
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING, null=True, blank=True)
    longitude = models.CharField('经度', max_length=20, null=True)
    latitude = models.CharField('纬度', max_length=20, null=True)

    def __str__(self):
        return self.name

    def tojson(self):
        hs = {}
        hs['id'] = self.id
        hs['name'] = self.name
        hs['englishname'] = self.englishname
        hs['word'] = self.word
        hs['worktime'] = self.worktime
        hs['price'] = self.price
        hs['pic1'] = str(self.pic1)
        hs['pic2'] = str(self.pic2)
        hs['pic3'] = str(self.pic3)
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
        hs['longitude'] = self.longitude
        hs['latitude'] = self.latitude
        hs['isfavour'] = 0
        if self.district:
            hs['district'] = self.district.tojson()
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


# 线路
class Route(models.Model):
    title = models.CharField('标题', max_length=100)
    time = models.DateTimeField('时间', null=True, blank=True)
    introduce = models.TextField('简介', max_length=500)
    hotspot = models.ManyToManyField(HotSpot)
    user = models.CharField('用户账号', max_length=50)

    def tojson(self):
        r = {}
        r['id'] = self.id
        r['title'] = self.title
        r['time'] = self.time
        r['introduce'] = self.introduce
        r['user'] = self.user
        r['hotspot'] = {'hotspot': []}
        for hs in self.hotspot.all():
            r['hotspot']['hotspot'].append(hs.tojson())
        return r
