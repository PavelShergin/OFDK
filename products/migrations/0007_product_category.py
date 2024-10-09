# Generated by Django 4.2.5 on 2023-12-26 17:28

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_productcategory_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=mptt.fields.TreeForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='articles', to='products.productcategory', verbose_name='Категория'),
            preserve_default=False,
        ),
    ]
