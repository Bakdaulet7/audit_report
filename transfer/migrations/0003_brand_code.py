# Generated by Django 2.1.4 on 2019-03-13 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0002_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='code',
            field=models.CharField(default='SOME STRING', max_length=50),
        ),
    ]
