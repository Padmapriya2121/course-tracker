from rest_framework import serializers
from .models import Progress, Alert

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Progress
        fields = ['id', 'user', 'lesson', 'completed_at']

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Alert
        fields = ['id', 'user', 'course', 'stage', 'progress', 'created_at']