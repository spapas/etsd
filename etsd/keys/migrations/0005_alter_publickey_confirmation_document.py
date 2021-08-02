# Generated by Django 3.2.5 on 2021-08-01 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("keys", "0004_auto_20210801_1722"),
    ]

    operations = [
        migrations.AlterField(
            model_name="publickey",
            name="confirmation_document",
            field=models.FileField(
                upload_to="public/confirmations/%Y/%m/%d/",
                verbose_name="Confirmation document",
            ),
        ),
    ]
