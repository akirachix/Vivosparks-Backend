from django.db import models

"""
Define the Quiz model, representing a quiz entity in the database
Auto-incrementing primary key
Text description of the quiz
Choices for scoring type: single or multiple choice
Scoring type field
Points or score for the quiz
"""


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_text = models.TextField()
    is_active = models.BooleanField(default=True)

    
    def soft_delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"Quiz {self.quiz_id}"


