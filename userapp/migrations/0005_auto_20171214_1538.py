# Generated by Django 2.0 on 2017-12-14 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_auto_20171214_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='access_token',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='验证头'),
        ),
    ]