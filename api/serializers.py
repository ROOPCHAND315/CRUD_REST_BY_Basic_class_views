from .models import StudentModel
from rest_framework import serializers

class StudentSerializer(serializers.ModelSerializer):
    def start_with_r(value):
        if value[0].lower() != 'r':
            raise serializers.ValidationError('Name should be start with R')

    name = serializers.CharField(validators=[start_with_r])

    class Meta:
        model=StudentModel
        fields='__all__'

    def validate_roll(self, value):
        if value >= 200:
            raise serializers.ValidationError('Seat Full')
        return value

 # Object Level Validation
    def validate(self, data):
        nm = data.get('name')
        ct = data.get('city')
        if nm.lower() == 'veeru' and ct.lower() != 'ranchi':
            raise serializers.ValidationError('City must be Ranchi')
        return data    