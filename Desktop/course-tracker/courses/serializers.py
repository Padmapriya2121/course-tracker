from rest_framework import serializers
from .models import Course, Module, Lesson, Enrollment

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Lesson
        fields = ['id', 'title', 'content', 'position']

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model  = Module
        fields = ['id', 'title', 'position', 'lessons']

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model  = Course
        fields = ['id', 'title', 'description', 'platform', 'created_at', 'modules']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at']