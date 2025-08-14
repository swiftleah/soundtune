from rest_framework import serializers
from .models import CustomUser

class UserSignupSerializer(serializers.ModelSerializer):
    #create extra field for confirm password -> not in CustomUser model
    confirm_password = serializers.CharField(write_only=True) #accepted as input but not returned in response

    class Meta:
        # define expected fields
        model = CustomUser
        #expected fields
        fields = ['full_name', 'email', 'password', 'confirm_password']
        #password is write only - not returned in serializer response (prevent sensitive info leaking)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        #validate unique email
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate(self, data):
        #validate matching passwords
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        #remove confirm_password - not part of our model
        validated_data.pop('confirm_password')

        #use custom user manager to create user
        user = CustomUser.objects.create_user(**validated_data) #dict of validated data received through serializer
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email']