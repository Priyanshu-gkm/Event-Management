# Generated by Django 4.2.6 on 2023-11-03 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_tickets', '0004_alter_photo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='archive',
            field=models.BooleanField(default=False, verbose_name='archive'),
        ),
    ]