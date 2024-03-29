# Generated by Django 3.0.2 on 2020-01-29 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20200128_1722'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Cart Item', 'verbose_name_plural': 'Cart Item'},
        ),
        migrations.AlterModelOptions(
            name='checkout',
            options={'verbose_name': 'Checkout', 'verbose_name_plural': 'Checkout List'},
        ),
        migrations.RemoveField(
            model_name='checkout',
            name='id',
        ),
        migrations.AddField(
            model_name='checkout',
            name='cartitem_ptr',
            field=models.OneToOneField(auto_created=True, default='', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.cartitem'),
            preserve_default=False,
        ),
    ]
