# Generated by Django 4.2.16 on 2024-09-11 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investment_simulation', '0004_rename_market_id_investmentsimulation_market'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investmentsimulation',
            old_name='market',
            new_name='market_id',
        ),
    ]
