from django.contrib.auth.models import User 
from rest_framework import serializers, validators


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    This model serializers is used to Register/Update users 
    """
    class Meta: 
        model = User 
        fields = ["email", "username", "password"] 
        extra_kwargs = {
            "password": {
                "write_only": True
            },

            # Ensure email is required and unique
            "email": {
                "required": True,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(),
                        message="A user with that email already exists",
                    )
                ]
            }
        }

    def create(self, validated_data):
        """
        Extra checking to ensure everything works well
        """
        password = validated_data.pop("password")
        instance = self.Meta.model(**validated_data) 
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance