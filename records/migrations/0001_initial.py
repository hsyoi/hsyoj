# Generated by Django 2.0.5 on 2018-05-25 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problems', '0002_auto_20180525_0518'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('submit_time', models.DateTimeField()),
                ('running_time', models.DurationField()),
                ('problem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='problems.Problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
    ]
