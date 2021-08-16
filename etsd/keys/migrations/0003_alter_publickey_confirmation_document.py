# Generated by Django 3.2.6 on 2021-08-15 19:50

from django.db import migrations, models
import etsd.keys.models


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publickey',
            name='confirmation_document',
            field=models.FileField(blank=True, null=True, upload_to=etsd.keys.models.confirmation_document_upload_to, verbose_name='Confirmation document'),
        ),
    ]
