# Generated by Django 2.1.5 on 2019-01-22 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast_log', '0015_podcast_episode_number_pattern'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='description',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]