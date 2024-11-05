from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserQuestion
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import requests
from .models import Profile, Lesson, Progress
from .serializers import ProfileSerializer, LessonSerializer, ProgressSerializer, AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to access this endpoint
def custom_auth_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def profile_detail_api(request, pk):
        
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Get a list of lessons or create a new lesson
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lesson_list_api(request):
    if request.method == 'GET':
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or delete a specific lesson by ID
@api_view(['GET', 'PUT', 'DELETE'])
def lesson_detail_api(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == 'GET':
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Progress API View
@api_view(['GET'])
def progress_detail_api(request, pk):
    progress = get_object_or_404(Progress, pk=pk)
    serializer = ProgressSerializer(progress, many=True)
    return Response(serializer.data)


#Update user progress
@api_view(['POST'])
def update_progress(request, lesson_id):

    profile = get_object_or_404(Profile, user=request.user)

    try:
        lesson = Lesson.objects.get(pk=lesson_id)
    except Lesson.DoesNotExist:
        return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)

    progress, created = Progress.objects.get_or_create(user=profile, lesson=lesson)
    progress.completion_percentage = request.data.get('completion_percentage', progress.completion_percentage)

    if progress.completion_percentage == 100.0:
        progress.completed = True

    progress.save()
    serializer = ProgressSerializer(progress)
    return Response(serializer.data, status=status.HTTP_200_OK)
