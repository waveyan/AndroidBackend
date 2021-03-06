# Generated by Django 2.0 on 2018-01-03 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotspotapp', '0007_auto_20180103_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('time', models.IntegerField(verbose_name='用时')),
                ('introduce', models.TextField(max_length=500, verbose_name='简介')),
                ('user', models.CharField(max_length=50, verbose_name='用户账号')),
                ('hotspot', models.ManyToManyField(to='hotspotapp.HotSpot')),
            ],
        ),
    ]
