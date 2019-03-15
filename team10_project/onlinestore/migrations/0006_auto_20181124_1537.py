# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-11-24 23:37
from __future__ import unicode_literals

from django.db import migrations
import onlinestore.formatChecker


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0005_auto_20181124_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=onlinestore.formatChecker.ContentTypeRestrictedFileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
