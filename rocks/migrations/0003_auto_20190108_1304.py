# Generated by Django 2.1.2 on 2019-01-08 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rocks', '0002_auto_20181230_1349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rock',
            options={'default_permissions': ('add', 'change', 'delete', 'view')},
        ),
    ]
