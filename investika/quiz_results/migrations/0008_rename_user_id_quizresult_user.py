# Generated by Django 4.2.16 on 2024-09-12 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_results', '0007_rename_result_id_quizresult_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizresult',
            old_name='user_id',
            new_name='user',
        ),
    ]