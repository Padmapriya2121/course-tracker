from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from users.models import User
from courses.models import Enrollment
from progress.models import Progress, Alert
from courses.models import Lesson

@api_view(['POST'])
def send_daily_email(request):
    users = User.objects.filter(role='student')
    emails_sent = 0

    for user in users:
        enrollments = Enrollment.objects.filter(user=user)
        if not enrollments:
            continue

        body = f"Hello {user.name},\n\nHere is your daily progress update:\n\n"

        for enrollment in enrollments:
            course  = enrollment.course
            total   = Lesson.objects.filter(module__course=course).count()
            completed = Progress.objects.filter(user=user, lesson__module__course=course).count()
            percentage = round((completed / total) * 100, 2) if total > 0 else 0

            if percentage <= 33:
                stage = '🔴 Red'
            elif percentage <= 66:
                stage = '🟡 Yellow'
            else:
                stage = '🟢 Green'

            body += f"Course: {course.title}\n"
            body += f"Progress: {percentage}%\n"
            body += f"Stage: {stage}\n"
            body += f"Streak: {user.streaks} days\n"
            body += f"Coins: {user.coins}\n\n"

        body += "Keep learning! 💪\n"

        send_mail(
            subject='Your Daily Progress Update',
            message=body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        emails_sent += 1

    return Response({'message': f'{emails_sent} emails sent successfully!'})