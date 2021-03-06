from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import json

from .models.groups import Group
from groups.models.groupMembers import GroupMember
from groups.models.groupCalendars import Calendar
from rooms.models import Room
from availability import dummyGroups
from students.models import Student

from students.serializers import StudentSerializer
from groups.serializers import CalendarSerializer
from matched_skills import lookingfor

def getGroupById(request, id=id):
  result = {}
  for group in Group.objects.all():
    if group.id == id:
      result = getGroupJson(group)
      break
  return JsonResponse(result, safe=False)

def index(request, id=id):
  groups = []
  for group in Group.objects.all():
      groups.append(getGroupJson(group))
  return JsonResponse(groups, safe=False)

def getPermission(request, gid, zid):
  result = {
    'inGroup': False,
    'isMember': False,
    'isOwner': False
  }
  for group in Group.objects.all():
    if (group.id == gid and group.owner.id == zid):
      result = {
        'inGroup': True,
        'isMember': True,
        'isOwner': True
      }
      return JsonResponse(result, safe=False)
  
  for groupMem in GroupMember.objects.all():
    if (groupMem.group.id == gid and groupMem.member.id == zid):
      if groupMem.status == True:
        result = {
          'inGroup': True,
          'isMember': True,
          'isOwner': False
        }
      else:
        result = {
          'inGroup': True,
          'isMember': False,
          'isOwner': False
        }
      break
  return JsonResponse(result, safe=False)

def getGroupByRoom(request, rid):
  groups = []
  for group in Group.objects.all():
    if group.room.id == rid:
      groups.append(getGroupJson(group))

  return JsonResponse(groups, safe=False)

def getGroupJson(group):
    photo = json.dumps(str(group.photo))
    id = group.id
    members = []
    members.append(StudentSerializer(group.owner).data)
    members = getMember(id, members)
    skills = getSkills(group.skills)
    currentSkills = getWeHave(group)
    vacancy = group.capacity - len(members) - 1
    events = getCalendar(id)
    result = {
      'id': group.id,
      'name': group.name, 
      'room': group.room.name,
      'owner': StudentSerializer(group.owner).data,
      'members': members,
      'descript': group.description,
      'location': group.preferredmeetingLoc,
      'photo': photo,
      'lookingFor': skills,
      'weHave': currentSkills,
      'capacity': group.capacity,
      'vacancy': vacancy,
      'events': events
    }

    return result

def getMember(id, members):
  for groupMem in GroupMember.objects.all():
    if (groupMem.group.id == id and groupMem.status):
      info = StudentSerializer(groupMem.member).data
      members.append(info)
  return members
 
def getSkills(skills):
  skills = skills.split(", ")
  return skills

def getWeHave(group):
  skills=""
  for grpMemb in GroupMember.objects.all():
    if (grpMemb.group == group):
      if skills:
        skills = skills + ", " + grpMemb.skills
      else :
        skills = grpMemb.skills
  if skills:
    weHaveSkills = skills.split(", ")
  else: 
    weHaveSkills = []
  return weHaveSkills

def getCalendar(id):
  events = []
  for event in Calendar.objects.all():
    if event.group.id == id:
      events.append(CalendarSerializer(event).data)
  return events

def addPhoto(request, gid, photo):
  result = {}
  group = Group.objects.get(id=gid)
  group.photo = photo
  group.save()
  return JsonResponse(result, safe=False)

def addDes(request, gid, descrip):
  result = {}
  group = Group.objects.get(id=gid)
  group.description = descrip
  group.save()
  result = {"description" : group.description}
  return JsonResponse(result, safe=False)

def addCalendar(request, gid):
  events = []
  group = Group.objects.get(id=gid)
  dummyEvents = dummyGroups[gid-1]
  for event in dummyEvents["preferredMeetingTimes"]:
        cal = Calendar.objects.create(
          group=group,
          eventName=event["name"],
          start=event["start"],
          end=event["end"]
        )
        cal.save()
        events.append(CalendarSerializer(cal).data)
  return JsonResponse(events, safe=False)

def deleteGroup(request, gid):
  result = {}
  group = Group.objects.get(id=gid)
  for member in GroupMember.objects.all():
        if (member.group == group):
              member.delete()
  group.delete()
  return JsonResponse(result, safe=False)

def joinGroup(request, gid, id):
  result = {}
  group = Group.objects.get(id=gid)
  skills = group.skills.split(", ")
  student = Student.objects.get(id=id)
  courses = []
  for course in student.courses.all():
    courses.append(course.name)
  matchedskills = lookingfor(skills, courses)

  group = Group.objects.get(id=gid)
  grpMemb = GroupMember.objects.create(
    group=group,
    member=student,
    status=True,
  )
  if matchedskills:
    grpMemb.skills=", ".join(matchedskills)
  grpMemb.save()

  newSkills = []
  for skill in skills:
    if skill not in matchedskills:
      newSkills.append(skill)
  group.skills = ", ".join(newSkills)
  group.save()
  return JsonResponse(result, safe=False)

def getRoomId(request, gid):
  group = Group.objects.get(id=gid)
  result = { "id": group.room.id }
  return JsonResponse(result, safe=False)

def leaveGroup(request, gid, id):
  result = {}
  group = Group.objects.get(id=gid)
  skills = group.skills.split(", ")
  student = Student.objects.get(id=id)
  matchedSkills = []
  for grpMemb in GroupMember.objects.all():
    if grpMemb.member.id == id and grpMemb.group.id == gid:
      matchedSkills=grpMemb.skills.split(", ")
      grpMemb.delete()
  for skill in matchedSkills:
      skills.append(skill)
  group.skills = ", ".join(skills)
  group.save()
  return JsonResponse(result, safe=False)