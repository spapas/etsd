# Generated by Django 3.2.6 on 2021-08-15 19:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("msgs", "0006_auto_20210813_1522"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="available_to_sender",
            field=models.BooleanField(
                default=True,
                help_text="The message is also encrypted with the sender's public key",
                verbose_name="Message is available to sender",
            ),
        ),
    ]
