# Generated by Django 2.1.3 on 2019-12-19 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0002_auto_20191219_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='park',
            name='uid',
            field=models.IntegerField(default=0),
        ),
    ]
