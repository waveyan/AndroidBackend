# Generated by Django 2.0 on 2018-01-04 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluationapp', '0005_auto_20180103_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='rate',
            field=models.CharField(default=0, max_length=2, verbose_name='评分'),
        ),
    ]
