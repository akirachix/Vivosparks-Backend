from django.db import models
from quizzes.models import Quiz 


"""
Define the QuizResult model, representing the results of a quiz in the database
Auto-incrementing primary key
Link to the related Quiz, cascades on delete
Score achieved in the quiz
Auto-populated completion date and time
Earnings with precision
"""

class QuizResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_on = models.DateTimeField(auto_now_add=True)
    money_earned = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)



    def soft_delete(self):
        """Mark this quiz result as inactive (soft delete)."""
        self.is_active = False
        self.save()

    def __str__(self):
        return f"Result {self.result_id} for Quiz {self.quiz.quiz_id}"

