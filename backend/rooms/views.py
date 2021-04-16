from django.shortcuts import render
from django.http import JsonResponse

from .models import Room
# Create your views here.
def index(request, id=id):
  rooms = []
  for room in Room.objects.all():
      rooms.append({
        'name': room.name
      })
  return JsonResponse(rooms, safe=False)