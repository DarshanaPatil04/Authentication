# Generated by Django 5.1.4 on 2025-01-13 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column1', models.CharField(max_length=100)),
                ('column2', models.CharField(max_length=100)),
                ('column3', models.IntegerField()),
            ],
        ),
    ]
