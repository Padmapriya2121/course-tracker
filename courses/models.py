from django.db import models

# Create your models here.

from users.models import User

class Course(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    platform    = models.CharField(max_length=20, default='manual')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    course   = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title    = models.CharField(max_length=200)
    position = models.IntegerField()

    def __str__(self):
        return self.title

class Lesson(models.Model):
    module   = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title    = models.CharField(max_length=200)
    content  = models.TextField(blank=True, null=True)
    position = models.IntegerField()

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    course    = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')