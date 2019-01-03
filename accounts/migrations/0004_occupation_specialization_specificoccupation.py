# Generated by Django 2.1.2 on 2019-01-03 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_auto_20190102_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'occupation',
            },
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'specialization',
            },
        ),
        migrations.CreateModel(
            name='SpecificOccupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation_id', models.ForeignKey(db_column='occupation_id', on_delete=django.db.models.deletion.PROTECT, to='accounts.Occupation')),
                ('specialization_id', models.ForeignKey(db_column='specialization_id', on_delete=django.db.models.deletion.PROTECT, to='accounts.Specialization')),
            ],
            options={
                'db_table': 'specific_occupation',
            },
        ),
    ]
