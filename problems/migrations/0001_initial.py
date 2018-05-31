# Generated by Django 2.0.5 on 2018-05-31 12:26

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True)),
                ('time_limit', models.FloatField(default=1.0)),
                ('memory_limit', models.FloatField(default=256.0)),
                ('description', models.TextField()),
                ('submissions', models.IntegerField(default=0)),
                ('accpected', models.IntegerField(default=0)),
            ],
            managers=[
                ('problems_set', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_content', models.TextField()),
                ('answer_content', models.TextField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.Problem')),
            ],
        ),
    ]
