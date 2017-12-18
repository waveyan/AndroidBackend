# Generated by Django 2.0 on 2017-12-18 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotspotapp', '0002_auto_20171218_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotspot',
            name='content',
            field=models.TextField(max_length=1000, verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='hotspot',
            name='name',
            field=models.CharField(max_length=50, verbose_name='地点名称'),
        ),
        migrations.AlterField(
            model_name='hotspot',
            name='pic',
            field=models.ImageField(upload_to='hotspot/', verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='hotspot',
            name='pic1_text',
            field=models.CharField(default='', max_length=200, null=True, verbose_name='图一解说'),
        ),
        migrations.AlterField(
            model_name='hotspot',
            name='pic2_text',
            field=models.CharField(default='', max_length=200, null=True, verbose_name='图二解说'),
        ),
        migrations.AlterField(
            model_name='hotspot',
            name='pic3_text',
            field=models.CharField(default='', max_length=200, null=True, verbose_name='图三解说'),
        ),
    ]