# Generated by Django 3.2.6 on 2021-09-15 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("authorities", "0003_authority_email"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserManagementLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created on"),
                ),
                (
                    "modified_on",
                    models.DateTimeField(auto_now=True, verbose_name="Modified on"),
                ),
                (
                    "removed_users",
                    models.TextField(blank=True, default="", editable=False),
                ),
                (
                    "added_users",
                    models.TextField(blank=True, default="", editable=False),
                ),
                (
                    "authority",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="authorities.authority",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="usermanagementlog_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="usermanagementlog_modified",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modified by",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
