# Generated by Django 3.2 on 2023-04-13 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20230413_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bancellphone',
            name='ban_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='banip',
            name='ban_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
