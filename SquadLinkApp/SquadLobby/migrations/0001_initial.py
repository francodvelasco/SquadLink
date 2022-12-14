# Generated by Django 3.2.12 on 2022-10-20 05:46

import SquadLobby.models
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('UserProfile', '0005_rename_regions_squadlinkusermodel_region'),
    ]

    operations = [
        migrations.CreateModel(
            name='SquadLinkLobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('squad_name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=280)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=SquadLobby.models.lobby_image_location)),
                ('platforms', models.CharField(blank=True, max_length=100)),
                ('game', models.CharField(blank=True, default='', max_length=100)),
                ('region', models.CharField(blank=True, max_length=100)),
                ('rank_lower_bound', models.CharField(max_length=100)),
                ('rank_higher_bound', models.CharField(max_length=100)),
                ('languages', models.CharField(max_length=300)),
                ('squad_size', models.IntegerField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserProfile.squadlinkusermodel')),
                ('squad_members', models.ManyToManyField(blank=True, related_name='members', to='UserProfile.SquadLinkUserModel')),
            ],
            managers=[
                ('custom_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
