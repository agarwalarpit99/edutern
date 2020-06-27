# Generated by Django 2.1.9 on 2020-06-25 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200622_2343'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('Join_Date', models.CharField(default='26/06/2020', max_length=50)),
                ('User_ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('User_FName', models.CharField(max_length=50)),
                ('User_LName', models.CharField(max_length=50)),
                ('User_Email', models.CharField(max_length=70)),
                ('User_Phone', models.CharField(max_length=15)),
                ('User_Password', models.CharField(max_length=20)),
                ('Verify_Status', models.CharField(default='Unverified', max_length=12)),
                ('Status', models.CharField(default='Active', max_length=10)),
            ],
            options={
                'db_table': 'UserData',
            },
        ),
    ]