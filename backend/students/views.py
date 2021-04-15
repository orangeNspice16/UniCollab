from django.shortcuts import render
from django.http import JsonResponse

from .models import Student
# Create your views here.

def index(request):
    students = []

    for student in Student.objects.all():
        students.append({
            'name': student.name,
            'course': student.course,
            'rating': student.rating
        })
    return JsonResponse(students, safe=False)


def user(request, id=id):
    user = {}
    for student in Student.objects.all():
        if (student.id == id):
            user = {
                'name': student.name,
                'course': student.course,
                'rating': student.rating
            }
            break
    return JsonResponse(user, safe=False)



# from rest_framework.viewsets import ModelViewSet

# from .models import Student
# from .serializers import StudentSerializer


# class StudentsViewSet(ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer