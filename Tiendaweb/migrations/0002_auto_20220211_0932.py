# Generated by Django 3.2.12 on 2022-02-11 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tiendaweb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagene',
            name='Img3',
        ),
        migrations.RemoveField(
            model_name='imagene',
            name='Recorte3',
        ),
    ]
