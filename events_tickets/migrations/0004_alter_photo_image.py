# Generated by Django 4.2.6 on 2023-11-02 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_tickets', '0003_alter_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.URLField(verbose_name='url'),
        ),
    ]
