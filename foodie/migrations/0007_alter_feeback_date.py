# Generated by Django 4.1.7 on 2023-03-11 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0006_alter_restaurant_time1_alter_restaurant_time2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeback',
            name='Date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
