# Generated by Django 2.0.6 on 2018-06-02 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_auto_20180602_2138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='language',
            new_name='compiler',
        ),
        migrations.RenameField(
            model_name='testcaseresult',
            old_name='status',
            new_name='result_code',
        ),
        migrations.RemoveField(
            model_name='record',
            name='status',
        ),
        migrations.AddField(
            model_name='record',
            name='accepted_flag',
            field=models.BooleanField(default=True, editable=False),
            preserve_default=False,
        ),
    ]