# Generated by Django 4.1.3 on 2024-03-08 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='complete',
            new_name='complate',
        ),
    ]
