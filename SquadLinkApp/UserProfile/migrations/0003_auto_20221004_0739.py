# Generated by Django 3.2.12 on 2022-10-04 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserProfile', '0002_auto_20221003_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='squadlinkusermodel',
            name='game',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='squadlinkusermodel',
            name='platforms',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='squadlinkusermodel',
            name='rank',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='squadlinkusermodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]