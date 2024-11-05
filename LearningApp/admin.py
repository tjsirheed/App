from django.contrib import admin
from .models import Profile, Lesson, Progress

# Register your models here.

def register_profile_admin():
    admin.site.register(
        Profile,
        list_display=('user', 'bio', 'profile_picture'), 
        fields=['user', 'bio', 'profile_pictuire']  
    )

register_profile_admin()

def register_Lesson_admin():
    admin.site.register(
        Lesson,
        list_display=('title', 'content', 'subject'), 
        fields=['title', 'content', 'subject']  
    )

register_Lesson_admin()


def register_Progress_admin():
    admin.site.register(
        Progress,
        list_display=('user', 'lesson', 'completion_percentage','completion_status'), 
        fields=['user', 'lesson', 'completion_percentage', 'completion_status']  
    )

register_Progress_admin()


