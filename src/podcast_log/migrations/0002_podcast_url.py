# Generated by Django 2.1.5 on 2019-01-15 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast_log', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
