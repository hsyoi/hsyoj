# Generated by Django 2.0.5 on 2018-06-02 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_auto_20180602_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='input_file_name',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='problem',
            name='optimize_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='problem',
            name='output_file_name',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='problem',
            name='stdio_flag',
            field=models.BooleanField(default=False),
        ),
    ]
