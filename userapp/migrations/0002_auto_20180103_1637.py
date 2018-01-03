# Generated by Django 2.0 on 2018-01-03 08:37

from django.db import migrations, models
import userapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pic',
            field=models.ImageField(default='pic/default.png', null=True, upload_to=userapp.models.upload_to, verbose_name='头像'),
        ),
    ]