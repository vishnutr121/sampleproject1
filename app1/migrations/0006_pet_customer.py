# Generated by Django 4.2.6 on 2023-11-24 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_pet_buystatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.customer'),
        ),
    ]