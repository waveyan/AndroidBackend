# Generated by Django 2.0 on 2018-01-05 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotspotapp', '0010_auto_20180104_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotspot',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hotspotapp.District'),
        ),
    ]