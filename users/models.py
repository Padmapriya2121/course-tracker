from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('mentor', 'Mentor'),
    ]
    name        = models.CharField(max_length=100)
    email       = models.EmailField(unique=True)
    password    = models.CharField(max_length=255)
    role        = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    streaks     = models.IntegerField(default=0)
    coins       = models.IntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name