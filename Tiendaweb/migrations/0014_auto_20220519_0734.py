# Generated by Django 3.2.12 on 2022-05-19 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tiendaweb', '0013_auto_20220517_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='Color',
        ),
        migrations.DeleteModel(
            name='Colore',
        ),
    ]
