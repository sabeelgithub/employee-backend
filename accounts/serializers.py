from rest_framework import serializers
from django.db import transaction

from accounts.models import CustomUser
class UserWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','username','email','phone','password']
    
    def validate_password(self, value):
        """
        Ensure the password is at least 5 characters long.
        """
        if len(value) < 5:
            raise serializers.ValidationError("Password must be at least 5 characters long.")
        return value
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        phone = validated_data.pop('phone',None)
        email = validated_data.pop('email',None)

        try:
            with transaction.atomic():
                user = CustomUser.objects.create(
                        username=username,
                        email=email,
                        phone=phone
                        ) 
                user.set_password(validated_data["password"])
                user.save()
                return user
        except Exception as e:
            raise serializers.ValidationError(f"Error Creating User: {str(e)}")
