# Generated by Django 3.0.2 on 2020-01-29 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_remove_wishitems_productcheck'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishitems',
            old_name='cartuser',
            new_name='wishuser',
        ),
        migrations.AddField(
            model_name='wishitems',
            name='wishstatus',
            field=models.CharField(default='', max_length=200),
        ),
    ]
