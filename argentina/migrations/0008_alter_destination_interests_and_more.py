# Generated by Django 4.0.6 on 2023-03-28 12:50

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('argentina', '0007_alter_trip_name_alter_tripdata_visited_destinations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='interests',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('FOOD', 'Food'), ('MUSIC', 'Music'), ('ART', 'Art'), ('TREKKING', 'Trekking'), ('ACTIVE', 'Active Activities'), ('RELAXING', 'Relaxing'), ('LANDSCAPES', 'Landscapes'), ('NATURE', 'Nature'), ('CULTURE', 'Culture')], max_length=65),
        ),
        migrations.AlterField(
            model_name='excursion',
            name='interests',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('FOOD', 'Food'), ('MUSIC', 'Music'), ('ART', 'Art'), ('TREKKING', 'Trekking'), ('ACTIVE', 'Active Activities'), ('RELAXING', 'Relaxing'), ('LANDSCAPES', 'Landscapes'), ('NATURE', 'Nature'), ('CULTURE', 'Culture')], max_length=65),
        ),
        migrations.AlterField(
            model_name='excursion',
            name='season',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], max_length=26),
        ),
        migrations.AlterField(
            model_name='tripdata',
            name='interests_selected',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('FOOD', 'Food'), ('MUSIC', 'Music'), ('ART', 'Art'), ('TREKKING', 'Trekking'), ('ACTIVE', 'Active Activities'), ('RELAXING', 'Relaxing'), ('LANDSCAPES', 'Landscapes'), ('NATURE', 'Nature'), ('CULTURE', 'Culture')], max_length=65),
        ),
        migrations.AlterField(
            model_name='tripdata',
            name='travel_season',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], max_length=26),
        ),
    ]