from rest_framework import serializers
from assessment.models import Assessment

class AssessmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Assessment model.

    This serializer converts Assessment model instances into JSON format
    and validates incoming JSON data before saving it to the database.
    """
    
    class Meta:
        model = Assessment
        fields = '__all__'  # Include all fields from the Assessment model in the serialization
