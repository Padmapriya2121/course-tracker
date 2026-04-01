from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User
from courses.models import Enrollment, Lesson
from progress.models import Progress

@api_view(['GET'])
def mentor_dashboard(request):
    students = User.objects.filter(role='student')
    dashboard = []

    for student in students:
        enrollments = Enrollment.objects.filter(user=student)
        courses_data = []

        for enrollment in enrollments:
            course    = enrollment.course
            total     = Lesson.objects.filter(module__course=course).count()
            completed = Progress.objects.filter(user=student, lesson__module__course=course).count()
            percentage = round((completed / total) * 100, 2) if total > 0 else 0

            if percentage <= 33:
                stage = 'red'
            elif percentage <= 66:
                stage = 'yellow'
            else:
                stage = 'green'

            courses_data.append({
                'course'     : course.title,
                'total'      : total,
                'completed'  : completed,
                'percentage' : f'{percentage}%',
                'stage'      : stage,
            })

        dashboard.append({
            'name'     : student.name,
            'email'    : student.email,
            'streaks'  : student.streaks,
            'coins'    : student.coins,
            'courses'  : courses_data,
        })

    return Response(dashboard)