# Generated by Django 2.1.2 on 2019-01-01 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('accounts', '0002_auto_20190102_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user2',
            name='user_ptr',
        ),
        migrations.DeleteModel(
            name='User2',
        ),
    ]
