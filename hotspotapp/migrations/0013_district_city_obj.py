# Generated by Django 2.0 on 2018-01-08 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotspotapp', '0012_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='city_obj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotspotapp.City'),
        ),
    ]
