# Generated by Django 4.2.3 on 2023-07-26 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elevator_number', models.IntegerField()),
                ('current_floor', models.PositiveSmallIntegerField(default=0)),
                ('is_operational', models.BooleanField(default=True)),
                ('is_door_open', models.BooleanField(default=True)),
                ('running_status', models.IntegerField(choices=[(1, 'Going Up'), (0, 'Not Moving'), (-1, 'Going Down')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ElevatorSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number_of_floor', models.IntegerField()),
                ('number_of_elevator', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ElevatorRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_floor', models.PositiveSmallIntegerField()),
                ('destination_floor', models.PositiveSmallIntegerField()),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('elevator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.elevator')),
            ],
        ),
        migrations.AddField(
            model_name='elevator',
            name='elevator_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.elevatorsystem'),
        ),
    ]