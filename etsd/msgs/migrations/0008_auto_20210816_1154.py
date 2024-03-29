# Generated by Django 3.2.6 on 2021-08-16 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("msgs", "0007_alter_message_available_to_sender"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="status",
            field=models.CharField(
                choices=[
                    ("UNREAD", "Unread"),
                    ("READ", "Read"),
                    ("ARCHIVED", "Archived"),
                ],
                default="UNREAD",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="available_to_sender",
            field=models.BooleanField(
                default=True,
                help_text="The message is also encrypted with the sender's public key. You need to select this to be able to see the data of your message.",
                verbose_name="Message is available to sender",
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="kind",
            field=models.CharField(
                choices=[("NEW", "New"), ("REPLY", "Reply"), ("FIX", "Fix")],
                help_text="If you select Reply or Fix you must also select the related message to which you reply or fix",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="rel_message",
            field=models.ForeignKey(
                blank=True,
                help_text="Please select a related message if needed",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="msgs.message",
                verbose_name="Related message",
            ),
        ),
    ]
