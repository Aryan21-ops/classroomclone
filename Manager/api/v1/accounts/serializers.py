from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={
            "input_type": "password",
        },
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={
            "input_type": "password",
            "label": "Confirm Password",
        },
    )

    def validate(self, data):
        user = User.objects.filter(email=data["email"])
        if user:
            user = user[0]

        if self.instance != None and self.instance.email != data['email']:
            if user:
                raise serializers.ValidationError(
                    {"email": "Email Address should be unique"}
                )
        elif user:
            raise serializers.ValidationError(
                {"email": "Email Address should be unique"}
            )
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password does not match."})
        return data

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]
