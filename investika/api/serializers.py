from rest_framework import serializers
from market.models import Market 
from investment_simulation.models import InvestmentSimulation
from quizzes.models import Quiz
from quiz_results.models import QuizResult
from assessment.models import Assessment
from django.contrib.auth.models import User
from virtualmoney.models import VirtualMoney
from achievements.models import Achievement
from users.models import User

        
"""      
Serializer for the Market model which include all fields in the serialized output  
"""
       
class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'
        
"""        
Serializer for the InvestmentSimulation model which include all fields in the serialized output
"""
class InvestmentSimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentSimulation
        fields = '__all__'
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




class AssessmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Assessment model.

    This serializer converts Assessment model instances into JSON format
    and validates incoming JSON data before saving it to the database.
    """
    
    class Meta:
        model = Assessment
        fields = '__all__'  # Include all fields from the Assessment model in the serialization



"""
This serializer is used to convert User model instances into JSON format and vice versa.
It is based on Django's `ModelSerializer`, which automatically handles the conversion between 
model instances and primitive data types (such as JSON).
The `Meta` class defines the fields that should be included in the serialized output 
 when retrieving or creating a user instance, including sensitive fields like `password`.

"""
 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = "__all__"

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Include all fields from the User model
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure the password is write-only
        }

    def create(self, validated_data):
        # Extract the password from validated_data
        password = validated_data.pop('password', None)
        
        # Create a new user using the remaining validated data
        user = User(**validated_data)
        
        # Set the password if it exists (use the `set_password` method to hash it)
        if password:
            user.set_password(password)
        
        # Save the user to the database
        user.save()
        
        return user

class VirtualMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualMoney
        fields = '__all__'
    
    def validate_amount(self, value):
        """Ensure the amount is not negative."""
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative")
        return value
class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['achievement_id', 'criteria', 'date_achieved', 'description', 'reward_type', 'title']
        

