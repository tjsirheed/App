from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserQuestion
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import requests
from .models import Profile, Lesson, Progress
from .serializers import ProfileSerializer, LessonSerializer, ProgressSerializer, AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

'''

from pydub import AudioSegment
import io
import speech_recognition as sr

'''


# Home Page with Gemini API integration

'''
@csrf_exempt
def ask_ai_question(request):
    if request.method == "POST":
        # Check if the question is in text or audio format
        question = request.POST.get('question', None)
        audio_file = request.FILES.get('audio', None)
        
        # Convert audio to text if audio is provided
        if audio_file:
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            try:
                question = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return JsonResponse({"error": "Could not understand the audio"}, status=400)
            except sr.RequestError:
                return JsonResponse({"error": "Speech Recognition service is unavailable"}, status=500)

        if not question:
            return JsonResponse({"error": "No question provided"}, status=400)

        # Send the question to the Gemini API
        gemini_api_url = settings.GEMINI_API_URL
        headers = {'Authorization': f"Bearer {settings.GEMINI_API_KEY}"}

        try:
            response = requests.post(gemini_api_url, json={'question': question}, headers=headers)
            answer = response.json().get('answer', 'No answer available')
        except requests.RequestException:
            return JsonResponse({"error": "Error fetching answer from Gemini"}, status=500)

        # Save the question and answer to the database
        if request.user.is_authenticated:
            UserQuestion.objects.create(user=request.user, question_text=question, answer_text=answer)

        
        return JsonResponse({"question": question, "answer": answer})

    return JsonResponse({"error": "Invalid request method"}, status=405)


'''

'''
@csrf_exempt
def ask_ai_question(request):
    if request.method == "POST":
        # Check if the question is in text or audio format
        question = request.POST.get('question', None)
        audio_file = request.FILES.get('audio', None)
        
        # Convert audio to text if audio is provided
        if audio_file:
            recognizer = sr.Recognizer()
            
            # Convert the uploaded audio to a WAV format compatible with SpeechRecognition
            audio_data = AudioSegment.from_file(io.BytesIO(audio_file.read()))
            wav_audio = io.BytesIO()
            audio_data.export(wav_audio, format="wav")
            wav_audio.seek(0)
            
            with sr.AudioFile(wav_audio) as source:
                audio = recognizer.record(source)
            try:
                question = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return JsonResponse({"error": "Could not understand the audio"}, status=400)
            except sr.RequestError:
                return JsonResponse({"error": "Speech Recognition service is unavailable"}, status=500)

        if not question:
            return JsonResponse({"error": "No question provided"}, status=400)

        # Send the question to the Gemini API
        gemini_api_url = settings.GEMINI_API_URL
        headers = {'Authorization': f"Bearer {settings.GEMINI_API_KEY}"}

        try:
            response = requests.post(gemini_api_url, json={'question': question}, headers=headers)
            answer = response.json().get('answer', 'No answer available')
        except requests.RequestException:
            return JsonResponse({"error": "Error fetching answer from Gemini"}, status=500)

        # Save the question and answer to the database 
        if request.user.is_authenticated:
            UserQuestion.objects.create(user=request.user, question_text=question, answer_text=answer)

        # Return the answer
        return JsonResponse({"question": question, "answer": answer})

    return JsonResponse({"error": "Invalid request method"}, status=405)


'''


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
    try:
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
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
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
    except Lesson.DoesNotExist:
        return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)

    progress, created = Progress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.completion_percentage = request.data.get('completion_percentage', progress.completion_percentage)

    if progress.completion_percentage == 100.0:
        progress.completed = True

    progress.save()
    serializer = ProgressSerializer(progress)
    return Response(serializer.data, status=status.HTTP_200_OK)
