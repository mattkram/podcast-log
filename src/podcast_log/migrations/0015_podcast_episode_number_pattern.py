# Generated by Django 2.1.5 on 2019-01-21 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast_log', '0014_auto_20190119_0344'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='episode_number_pattern',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
