# Generated by Django 2.1.2 on 2019-02-16 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0002_auto_20190108_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='checksum',
            field=models.CharField(default='asdasd', max_length=64),
            preserve_default=False,
        ),
    ]
