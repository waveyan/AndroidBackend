# Generated by Django 2.0 on 2018-01-08 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluationapp', '0009_auto_20180104_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='usr_like',
            field=models.ManyToManyField(related_name='evaluation_like_set', to='userapp.User'),
        ),
    ]
