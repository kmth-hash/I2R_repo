# Generated by Django 3.0.5 on 2021-05-26 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproj', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
