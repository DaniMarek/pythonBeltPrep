# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-03 16:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0004_remove_item_starting_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='bidder',
        ),
    ]
