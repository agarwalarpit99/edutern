# Generated by Django 2.1.9 on 2020-06-22 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseData',
            fields=[
                ('Course_ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Course_Name', models.CharField(max_length=100)),
                ('Course_Trainer', models.CharField(max_length=100)),
                ('Course_Fee', models.CharField(max_length=50)),
                ('Course_Objective', models.CharField(max_length=1000)),
                ('Course_Eligibility', models.CharField(max_length=1000)),
                ('Course_Contents', models.CharField(max_length=1000)),
                ('Course_Thumb', models.FileField(upload_to='coursethumb/')),
            ],
            options={
                'db_table': 'CourseData',
            },
        ),
    ]