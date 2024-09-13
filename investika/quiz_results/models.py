from django.db import models
from quizzes.models import Quiz 
from users.models import User
from django.conf import settings
from django.contrib.auth import get_user_model


"""
Define the QuizResult model, representing the results of a quiz in the database
Auto-incrementing primary key
Link to the related Quiz, cascades on delete
Score achieved in the quiz
Auto-populated completion date and time
Earnings with precision
"""
User = get_user_model()
class QuizResult(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,default=None)
    score = models.IntegerField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    money_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Example field

    def soft_delete(self):
        """Mark this quiz result as inactive (soft delete)."""
        self.is_active = False
        self.save()

    def __str__(self):
        return f"Result {self.result_id} for Quiz {self.quiz.quiz_id}"

