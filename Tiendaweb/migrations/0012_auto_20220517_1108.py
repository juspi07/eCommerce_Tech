# Generated by Django 3.2.12 on 2022-05-17 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tiendaweb', '0011_alter_colore_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='Desc',
            field=models.TextField(default='asd', max_length=60),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producto',
            name='fecha_alta',
            field=models.DateField(auto_now_add=True, verbose_name='Fecha de Alta'),
        ),
    ]
