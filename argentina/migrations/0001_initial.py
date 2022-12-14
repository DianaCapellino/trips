# Generated by Django 4.0.6 on 2022-09-11 02:05

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('pic1_url', models.CharField(max_length=500)),
                ('pic2_url', models.CharField(max_length=500)),
                ('pic3_url', models.CharField(max_length=500)),
                ('atractions', multiselectfield.db.fields.MultiSelectField(choices=[('CITY', 'City'), ('FALLS', 'Falls'), ('MOUNTAINS', 'Mountains'), ('COUNTRYSIDE', 'Countryside'), ('GLACIERS', 'Glaciers'), ('WILDLIFE', 'Wildlife')], max_length=50)),
                ('interests', multiselectfield.db.fields.MultiSelectField(choices=[('FOOD', 'Food'), ('MUSIC', 'Music'), ('ART', 'Art'), ('TREKKING', 'Trekking'), ('ACTIVE', 'Active Activities'), ('RELAXING', 'Relaxing')], max_length=39)),
                ('min_nights', models.PositiveSmallIntegerField()),
                ('max_nights', models.PositiveSmallIntegerField()),
                ('children_ranking', multiselectfield.db.fields.MultiSelectField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Excursion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1500)),
                ('pic1_url', models.CharField(max_length=500)),
                ('pic2_url', models.CharField(max_length=500)),
                ('pic3_url', models.CharField(max_length=500)),
                ('season', multiselectfield.db.fields.MultiSelectField(choices=[('JANUARY', 'January'), ('FEBRUARY', 'February'), ('MARCH', 'March'), ('APRIL', 'April'), ('MAY', 'May'), ('JUNE', 'June'), ('JULY', 'July'), ('AUGUST', 'August'), ('SEPTEMBER', 'September'), ('OCTOBER', 'October'), ('NOVEMBER', 'November'), ('DECEMBER', 'December')], max_length=85)),
                ('interests', multiselectfield.db.fields.MultiSelectField(choices=[('FOOD', 'Food'), ('MUSIC', 'Music'), ('ART', 'Art'), ('TREKKING', 'Trekking'), ('ACTIVE', 'Active Activities'), ('RELAXING', 'Relaxing')], max_length=39)),
                ('min_age', models.PositiveSmallIntegerField()),
                ('max_age', models.PositiveSmallIntegerField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='excursions', to='argentina.destination')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_quality', multiselectfield.db.fields.MultiSelectField(choices=[(3, '3'), (4, '4'), (5, '5')], max_length=5)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=800)),
                ('picture1', models.CharField(max_length=500)),
                ('pic2_url', models.CharField(max_length=500)),
                ('pic3_url', models.CharField(max_length=500)),
                ('min_age', models.PositiveSmallIntegerField()),
                ('max_age', models.PositiveSmallIntegerField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='argentina.destination')),
            ],
        ),
        migrations.CreateModel(
            name='TripExcursions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dayInTrip', models.PositiveSmallIntegerField()),
                ('excursion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_excursions', to='argentina.excursion')),
            ],
        ),
        migrations.CreateModel(
            name='TripDestination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nights', models.PositiveSmallIntegerField()),
                ('orderInTrip', models.PositiveSmallIntegerField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='argentina.destination')),
                ('excursions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_excursions', to='argentina.tripexcursions')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stay', to='argentina.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='TripData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('are_children', models.BooleanField(default=False)),
                ('max_age', models.PositiveSmallIntegerField()),
                ('num_pax', models.PositiveSmallIntegerField()),
                ('num_days', models.PositiveSmallIntegerField()),
                ('atractions_selected', multiselectfield.db.fields.MultiSelectField(choices=[('CITY', 'City'), ('FALLS', 'Falls'), ('MOUNTAINS', 'Mountains'), ('COUNTRYSIDE', 'Countryside'), ('GLACIERS', 'Glaciers'), ('WILDLIFE', 'Wildlife')], max_length=50)),
                ('interests_selected', multiselectfield.db.fields.MultiSelectField(choices=[('FOOD', 'Food'), ('MUSIC', 'Music'), ('ART', 'Art'), ('TREKKING', 'Trekking'), ('ACTIVE', 'Active Activities'), ('RELAXING', 'Relaxing')], max_length=39)),
                ('travel_season', multiselectfield.db.fields.MultiSelectField(choices=[('JANUARY', 'January'), ('FEBRUARY', 'February'), ('MARCH', 'March'), ('APRIL', 'April'), ('MAY', 'May'), ('JUNE', 'June'), ('JULY', 'July'), ('AUGUST', 'August'), ('SEPTEMBER', 'September'), ('OCTOBER', 'October'), ('NOVEMBER', 'November'), ('DECEMBER', 'December')], max_length=85)),
                ('hotel_quality_selected', multiselectfield.db.fields.MultiSelectField(choices=[(3, '3'), (4, '4'), (5, '5')], max_length=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_user', to=settings.AUTH_USER_MODEL)),
                ('visited_destinations', models.ManyToManyField(related_name='visited', to='argentina.destination')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('nights', models.PositiveSmallIntegerField()),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='start_date')),
                ('finish_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='finish_date')),
                ('destinations', models.ManyToManyField(related_name='trip_destinations', to='argentina.tripdestination')),
                ('shared_with', models.ManyToManyField(related_name='companions_trip', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now=True, verbose_name='comment_date')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_trip', to='argentina.trip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
