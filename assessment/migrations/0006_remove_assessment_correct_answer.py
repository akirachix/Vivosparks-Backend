# Generated by Django 4.2 on 2024-09-18 08:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("assessment", "0005_remove_assessment_investment_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assessment",
            name="correct_answer",
        ),
    ]
