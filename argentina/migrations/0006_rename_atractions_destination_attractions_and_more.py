# Generated by Django 4.0.6 on 2022-09-17 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('argentina', '0005_rename_picture1_hotel_pic1_url_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='destination',
            old_name='atractions',
            new_name='attractions',
        ),
        migrations.RenameField(
            model_name='tripdata',
            old_name='atractions_selected',
            new_name='attractions_selected',
        ),
    ]
