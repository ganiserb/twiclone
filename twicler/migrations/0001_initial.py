# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Twiclo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('user_ptr', models.OneToOneField(serialize=False, primary_key=True, parent_link=True, auto_created=True, to=settings.AUTH_USER_MODEL)),
                ('visibility', models.CharField(max_length=2, default='PU', choices=[('PU', 'Public'), ('FI', 'Those I follow')])),
                ('followers', models.ManyToManyField(related_name='followers_rel_+', to='twicler.UserSettings')),
                ('following', models.ManyToManyField(related_name='following_rel_+', to='twicler.UserSettings')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
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
