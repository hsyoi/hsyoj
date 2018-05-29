# Generated by Django 2.0.5 on 2018-05-29 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_auto_20180526_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='language',
            field=models.CharField(choices=[('c', 'C'), ('cpp', 'C++')], default='C', editable=False, max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='record',
            name='problem',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='problems.Problem'),
        ),
        migrations.AlterField(
            model_name='record',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
    ]