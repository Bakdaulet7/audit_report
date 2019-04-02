# Generated by Django 2.1.4 on 2019-03-13 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counterparty', models.CharField(max_length=50)),
                ('sector', models.CharField(max_length=30)),
                ('sku', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('status', models.IntegerField()),
            ],
        ),
    ]
