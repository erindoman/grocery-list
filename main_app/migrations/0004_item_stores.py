# Generated by Django 3.1.5 on 2021-02-02 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20210202_0444'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stores',
            field=models.ManyToManyField(to='main_app.Store'),
        ),
    ]