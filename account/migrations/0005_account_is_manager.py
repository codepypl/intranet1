# Generated by Django 4.0.4 on 2022-05-14 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_account_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_manager',
            field=models.BooleanField(default=False, verbose_name='is_manager'),
        ),
    ]
