# Generated by Django 2.0 on 2017-12-14 06:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotspotapp', '0001_initial'),
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=200, verbose_name='评论')),
                ('time', models.DateTimeField(default=datetime.datetime.now, verbose_name='时间')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=0, verbose_name='评分')),
                ('feeling', models.CharField(max_length=200, verbose_name='心情')),
                ('pic', models.ImageField(null=True, upload_to='', verbose_name='游玩图片')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='消费')),
                ('likes', models.IntegerField(default=0, verbose_name='点赞数')),
                ('time', models.DateTimeField(default=datetime.datetime.now, verbose_name='时间')),
                ('hotspot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotspotapp.HotSpot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.User')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='evaluation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluationapp.Evaluation'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.User'),
        ),
    ]