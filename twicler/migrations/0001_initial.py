# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Twiclo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('text', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False, auto_created=True, parent_link=True)),
                ('visibility', models.CharField(max_length=2, default='PU', choices=[('PU', 'Public'), ('FI', 'Those I follow')])),
                ('followers', models.ManyToManyField(to='twicler.UserSettings', related_name='followers_rel_+')),
                ('following', models.ManyToManyField(to='twicler.UserSettings', related_name='following_rel_+')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='twiclo',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
