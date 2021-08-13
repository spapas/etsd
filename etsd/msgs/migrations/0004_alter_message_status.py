# Generated by Django 3.2.6 on 2021-08-12 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msgs', '0003_alter_message_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Draft'), ('SENT', 'Sent'), ('READ', 'Read'), ('ARCHIVED', 'Archived'), ('DELETED', 'Deleted')], default='DRAFT', max_length=32),
        ),
    ]