# Generated by Django 3.2.12 on 2022-02-11 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tiendaweb', '0005_alter_producto_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='Nombre',
            field=models.CharField(default='gola', max_length=20),
            preserve_default=False,
        ),
    ]
