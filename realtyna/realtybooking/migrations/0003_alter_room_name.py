# Generated by Django 4.2.5 on 2023-09-26 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtybooking', '0002_alter_reservation_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
