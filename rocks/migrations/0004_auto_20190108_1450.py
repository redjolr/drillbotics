# Generated by Django 2.1.2 on 2019-01-08 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rocks', '0003_auto_20190108_1304'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rock',
            options={'default_permissions': ('view', 'add', 'change', 'delete')},
        ),
    ]
