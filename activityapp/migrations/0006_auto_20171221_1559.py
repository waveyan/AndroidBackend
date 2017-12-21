# Generated by Django 2.0 on 2017-12-21 07:59

import activityapp.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activityapp', '0005_auto_20171221_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='hotspot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotspotapp.HotSpot'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='pic1',
            field=models.ImageField(blank=True, default='activity/default.png', null=True, upload_to=activityapp.models.upload_to, verbose_name='活动图片1'),
        ),
    ]
