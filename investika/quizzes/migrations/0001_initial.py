# Generated by Django 5.1.1 on 2024-09-08 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('quiz_text', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]