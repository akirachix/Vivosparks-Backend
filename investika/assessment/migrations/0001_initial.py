# Generated by Django 5.1.1 on 2024-09-06 09:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
