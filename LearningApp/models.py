from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Lesson(models.Model):
    SUBJECT_CHOICES = [
        ('Math', 'Mathematics'),
        ('English', 'English Language'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
    ]
    title = models.CharField(max_length=100)
    content = models.TextField()
    subject = models.CharField(max_length=50, choices = SUBJECT_CHOICES, default = 'Math')

    def __str__(self):
        return f"{self.title}({self.get_subject_display()})"

class Progress(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    completion_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.user.username if self.user else 'No user'}'s Progress in {self.lesson.title}"
    

class UserQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

