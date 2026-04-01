from django.db import models

# Create your models here.

from users.models import User
from courses.models import Lesson, Course

class Progress(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson       = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.name} - {self.lesson.title}"

class Alert(models.Model):
    STAGE_CHOICES = [
        ('red', 'Red'),
        ('yellow', 'Yellow'),
        ('green', 'Green'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    course     = models.ForeignKey(Course, on_delete=models.CASCADE)
    stage      = models.CharField(max_length=10, choices=STAGE_CHOICES)
    progress   = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.stage}"