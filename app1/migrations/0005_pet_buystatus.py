# Generated by Django 4.2.6 on 2023-11-24 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_pet_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='buystatus',
            field=models.CharField(default='not sold', max_length=255),
        ),
    ]
