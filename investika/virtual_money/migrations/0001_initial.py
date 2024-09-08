# Generated by Django 4.2.16 on 2024-09-08 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualMoney',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_granted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
