# Generated by Django 3.2.6 on 2021-08-19 05:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("msgs", "0011_message_local_protocol"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="local_protocol",
            field=models.CharField(
                blank=True,
                help_text="Please provide a local identifier (local authority protocol) if needed.",
                max_length=50,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Valid characters are 0-9 . - /", regex="^[#](\\w+)$"
                    )
                ],
                verbose_name="Local identifier",
            ),
        ),
    ]
