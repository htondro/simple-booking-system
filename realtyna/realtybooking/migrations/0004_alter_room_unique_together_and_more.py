# Generated by Django 4.2.5 on 2023-09-26 10:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('realtybooking', '0003_alter_room_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('name', 'owner')},
        ),
        migrations.AddIndex(
            model_name='reservation',
            index=models.Index(fields=['room', '-start_date', '-end_date'], name='realtybooki_room_id_ab435d_idx'),
        ),
    ]
