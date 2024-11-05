from rest_framework import serializers
from .models import Profile, Lesson, Progress
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_picture']

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if user is None:
                raise serializers.ValidationError(_('Invalid username or password.'))
        else:
            raise serializers.ValidationError(_('Must include "username" and "password".'))

        attrs['user'] = user
        return attrs


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'subject']

class ProgressSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='user__username', queryset=Profile.objects.all())
    lesson = serializers.SlugRelatedField(slug_field='title', queryset=Lesson.objects.all())

    class Meta:
        model = Progress
        fields = ['user', 'lesson', 'completion_percentage','completion_status']

                