# Generated by Django 4.0.6 on 2022-09-14 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('argentina', '0003_alter_destination_children_ranking_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='children_ranking',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], max_length=10),
        ),
        migrations.AlterField(
            model_name='tripdata',
            name='hotel_quality_selected',
            field=models.CharField(choices=[(3, '3'), (4, '4'), (5, '5')], max_length=10),
        ),
    ]
