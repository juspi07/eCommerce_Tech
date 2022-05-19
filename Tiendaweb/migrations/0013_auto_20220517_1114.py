# Generated by Django 3.2.12 on 2022-05-17 14:14

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Tiendaweb', '0012_auto_20220517_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagene',
            name='Img3',
            field=models.ImageField(default='', upload_to='img_productos/', verbose_name='Imagen 3:'),
        ),
        migrations.AddField(
            model_name='imagene',
            name='Img4',
            field=models.ImageField(default='', upload_to='img_productos/', verbose_name='Imagen 4:'),
        ),
        migrations.AddField(
            model_name='imagene',
            name='Recorte3',
            field=image_cropping.fields.ImageRatioField('Img3', '277x377', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='Recorte3'),
        ),
        migrations.AddField(
            model_name='imagene',
            name='Recorte4',
            field=image_cropping.fields.ImageRatioField('Img4', '277x377', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='Recorte4'),
        ),
    ]