from django.urls import path
from . import views


urlpatterns = [
    #path('api/ask_ai/', views.ask_ai_question, name='ask_ai'),

    path('LearningApp/auth/login/', views.custom_auth_token, name='login'),

    path('LearningApp/profile/<int:pk>/', views.profile_detail_api, name='profile_detail_api'),

    path('LearningApp/profile/update/', views.update_profile, name='update_profile'),

    path('LearningApp/lessons/', views.lesson_list_api, name='lesson_list_api'),

    path('LearningApp/lessons/<int:pk>/', views.lesson_detail_api, name='lesson_detail_api'),

    path('LearningApp/progress/<int:pk>/', views.progress_detail_api, name='progress_detail_api'),

    path('LearningApp/progress/update/<int:lesson_id>/', views.update_progress, name='update_progress'),
]

