# Generated by Django 3.2.12 on 2022-10-07 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0003_auto_20221004_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='squadlinkusermodel',
            name='bio',
            field=models.CharField(blank=True, default='', max_length=280),
        ),
        migrations.AddField(
            model_name='squadlinkusermodel',
            name='regions',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]