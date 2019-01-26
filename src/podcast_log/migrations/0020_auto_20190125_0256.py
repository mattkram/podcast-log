# Generated by Django 2.1.5 on 2019-01-25 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast_log', '0019_auto_20190122_1831'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episode',
            old_name='image_url',
            new_name='_image_url',
        ),
        migrations.AlterField(
            model_name='episode',
            name='status',
            field=models.CharField(choices=[('Q', 'Queued'), ('L', 'Listened'), ('P', 'In Progress'), ('S', 'Skipped'), ('I', 'Ignored')], default='Q', max_length=1),
        ),
    ]