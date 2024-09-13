# Generated by Django 4.2.16 on 2024-09-11 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('assessment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('spending_on_wants', models.DecimalField(decimal_places=2, max_digits=10)),
                ('spending_on_needs', models.DecimalField(decimal_places=2, max_digits=10)),
                ('savings', models.DecimalField(decimal_places=2, max_digits=10)),
                ('investment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('taken_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]