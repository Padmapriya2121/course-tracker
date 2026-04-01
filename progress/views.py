from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Progress, Alert
from .serializers import ProgressSerializer, AlertSerializer
from courses.models import Lesson, Enrollment
from users.models import User

# POST /api/progress/complete/
@api_view(['POST'])
def complete_lesson(request):
    serializer = ProgressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Calculate progress and update alert
        user_id   = request.data.get('user')
        lesson    = Lesson.objects.get(id=request.data.get('lesson'))
        course    = lesson.module.course
        total     = Lesson.objects.filter(module__course=course).count()
        completed = Progress.objects.filter(user_id=user_id, lesson__module__course=course).count()
        percentage = round((completed / total) * 100, 2)
        # Determine stage
        if percentage <= 33:
            stage = 'red'
        elif percentage <= 66:
            stage = 'yellow'
        else:
            stage = 'green'
        # Save alert
        Alert.objects.create(user_id=user_id, course=course, stage=stage, progress=percentage)
        return Response({
            'message'    : 'Lesson completed!',
            'progress'   : f'{percentage}%',
            'stage'      : stage,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /api/progress/?user_id=1&course_id=1
@api_view(['GET'])
def get_progress(request):
    user_id   = request.query_params.get('user_id')
    course_id = request.query_params.get('course_id')
    total     = Lesson.objects.filter(module__course_id=course_id).count()
    completed = Progress.objects.filter(user_id=user_id, lesson__module__course_id=course_id).count()
    percentage = round((completed / total) * 100, 2) if total > 0 else 0
    if percentage <= 33:
        stage = 'red'
    elif percentage <= 66:
        stage = 'yellow'
    else:
        stage = 'green'
    return Response({
        'user_id'    : user_id,
        'course_id'  : course_id,
        'total'      : total,
        'completed'  : completed,
        'percentage' : f'{percentage}%',
        'stage'      : stage,
    })