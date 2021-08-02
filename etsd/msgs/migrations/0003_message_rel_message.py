# Generated by Django 3.2.5 on 2021-08-02 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("msgs", "0002_auto_20210802_0831"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="rel_message",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="msgs.message",
                verbose_name="Related message",
            ),
        ),
    ]
