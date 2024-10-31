from django.urls import path
from . import views


urlpatterns = [
    #path('api/ask_ai/', views.ask_ai_question, name='ask_ai'),

    path('api/auth/login/', views.custom_auth_token, name='login'),

    path('api/profile/<int:pk>/', views.profile_detail_api, name='profile_detail_api'),

    path('api/profile/update/<int:pk>', views.update_profile, name='update_profile'),

    path('api/lessons/', views.lesson_list_api, name='lesson_list_api'),

    path('api/lessons/<int:pk>/', views.lesson_detail_api, name='lesson_detail_api'),

    path('api/progress/<int:pk>/', views.progress_detail_api, name='progress_detail_api'),

    path('api/progress/update/<int:lesson_id>/', views.update_progress, name='update_progress'),
]

