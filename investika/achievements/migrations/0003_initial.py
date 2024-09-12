# Generated by Django 5.1.1 on 2024-09-11 20:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('achievements', '0002_rename_achievement_id_achievement_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('criteria', models.TextField()),
                ('date_achieved', models.DateField()),
                ('description', models.TextField()),
                ('reward_type', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('user_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='achievements_in_achievements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
