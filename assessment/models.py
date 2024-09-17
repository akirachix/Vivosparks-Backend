from django.db import models
from django.conf import settings

class Assessment(models.Model):
    """
    Represents an assessment taken by a user, including associated questions.
    
    Attributes:
    assessment_id: Unique identifier for each assessment (Primary Key).
    user_id: Reference to the user who took the assessment (Foreign Key).
    question_text: The text of the question associated with the assessment.
    question_image: URL of an optional image related to the question.
    answers: A JSON field storing possible answers to the question.
    correct_answer: The correct answer for the question (if applicable).
    is_active: Indicator for whether the assessment is active (supports soft deletion).
    taken_at: Timestamp for when the assessment was taken.
    """

    assessment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)
    question_text = models.CharField(max_length=255, default=None)
    question_image = models.URLField(max_length=255, null=True, blank=True)
    answers = models.JSONField(default=list)  
    correct_answer = models.CharField(max_length=255, blank=True)  
    is_active = models.BooleanField(default=True)
    taken_at = models.DateTimeField(auto_now_add=True)  

    def soft_delete(self):
        """Soft delete the assessment by marking it as inactive."""
        self.is_active = False
        self.save()

    def __str__(self):
        return f"Assessment {self.assessment_id} by User {self.user_id}"
