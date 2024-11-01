from rest_framework import serializers

from .models import Employee

class EmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','name','email','position','custom_fields']
    
    def create(self, validated_data):
        user = self.context['user']
        validated_data['user'] = user
        return super().create(validated_data)


class EmployeeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','name','email','position','custom_fields','created_at','updated_at']

