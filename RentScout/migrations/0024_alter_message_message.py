# Generated by Django 4.2.4 on 2024-12-23 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RentScout', '0023_alter_message_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
