# Generated by Django 2.1.2 on 2018-12-15 18:26

from django.db import migrations, models
import django.db.models.deletion
import sensors.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sensors', '0001_initial'),
        ('rocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('description', models.TextField()),
                ('rock_id', models.ForeignKey(db_column='rock_id', on_delete=django.db.models.deletion.PROTECT, to='rocks.Rock')),
            ],
            options={
                'db_table': 'experiment',
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_micro', models.BigIntegerField(verbose_name=sensors.models.Sensor)),
                ('value', models.FloatField()),
                ('depth', models.FloatField(null=True)),
                ('experiment_id', models.ForeignKey(db_column='experiment_id', on_delete=django.db.models.deletion.CASCADE, to='experiments.Experiment')),
                ('sensor_id', models.ForeignKey(db_column='sensor_id', on_delete=django.db.models.deletion.PROTECT, to='sensors.Sensor')),
            ],
            options={
                'db_table': 'measurement',
            },
        ),
    ]