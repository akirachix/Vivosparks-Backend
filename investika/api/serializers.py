from rest_framework import serializers
from quizzes.models import Quiz
from quiz_results.models import QuizResult



"""
Serializer for the Quiz model, handling all fields of the model
Specify the model the serializer should use
Use all fields of the Quiz model
"""
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"

"""
Serializer for the QuizResult model, handling all fields of the model
Specify the model the serializer should use
Use all fields of the QuizResult model
"""
class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = "__all__"



