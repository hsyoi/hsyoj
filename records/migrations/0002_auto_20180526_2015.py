# Generated by Django 2.0.5 on 2018-05-26 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='code',
            field=models.TextField(editable=False),
        ),
        migrations.AlterField(
            model_name='record',
            name='running_time',
            field=models.DurationField(editable=False),
        ),
    ]
