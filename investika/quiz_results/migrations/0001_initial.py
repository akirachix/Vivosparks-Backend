# Generated by Django 5.1.1 on 2024-09-08 08:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('result_id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField()),
                ('completed_on', models.DateTimeField(auto_now_add=True)),
                ('money_earned', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.quiz')),
            ],
        ),
    ]
