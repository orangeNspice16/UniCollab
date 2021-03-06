from django.shortcuts import render
from django.http import JsonResponse
import json 

from students.serializers import StudentSerializer, EventSerializer
from groups.serializers import CalendarSerializer


from groups.models.groups import Group
from groups.models.groupMembers import GroupMember
from .models import Room, Member
from students.models import Student
from meeting import sortGroupByDistance
from groups.models.groupCalendars import Calendar
from availability import sortGroupByAvailabilities
from matched_skills import lookingfor
from skills import sortGroupBySkills
from overall import sortOverallGroups

# Create your views here.
def index(request, id=id):
  rooms = []
  for room in Room.objects.all():
      rooms.append({
        'name': room.name,
        'id': room.id,
        'description': room.description,
        'members' : getRoomMember(room.id)
      })
  return JsonResponse(rooms, safe=False)

def getRoomById(request, id=id):
  result = {}
  for room in Room.objects.all():
    if room.id == id:
      members = getRoomMember(id)
      result = {
        'name': room.name,
        'id': room.id,
        'description': room.description,
        'members': members
      }
      break
  return JsonResponse(result, safe=False)

def getRoomMember(id):
  roomMembers = []
  for memb in Member.objects.all():
    if (memb.room.id == id):
      info = StudentSerializer(memb.student).data
      roomMembers.append(info)
  return roomMembers
      
def joinRoom(request, id, rid):
  student = Student.objects.get(id=id)
  for room in Room.objects.all():
    if (room.id == rid):
      room.members.add(student)
  return rid
  

def getStudentJson(id):
  student = Student.objects.get(id=id)
  calendar = getStudentCal(student)
  student = {
    "location" : student.location,
    "calendar" : calendar
  }
  return student

def getStudentCal(student):
  events = []
  for event in student.calendar.all():
      events.append(EventSerializer(event).data)
  return events

def createGroup(request, id, rid, name):
  groupRet = {}
  student = Student.objects.get(id=id)
  room = Room.objects.get(id=rid)
  group = Group.objects.create(
    room=room,
    owner=student,
    name=name,
    preferredmeetingLoc=student.location
  )
  group.save()
  groupRet = { "id" : group.id }
  return JsonResponse(groupRet, safe=False)

def getLocation(request, id, rid):
  groups = []
  student = getStudentJson(id)
  for group in Group.objects.all():
    if group.room.id == rid:
      groups.append(getGroupJson(group))
  sortedGroups = sortGroupByDistance(groups, student)
  return JsonResponse(sortedGroups, safe=False)

def getGroupJson(group):
    photo = json.dumps(str(group.photo))
    id = group.id
    members = getMember(id)
    vacancy = group.capacity - len(members)
    calendar = getCalendar(id)
    wehave = getWeHave(group)
    result = {
      'id': group.id,
      'name': group.name, 
      'members': members,
      'descript': group.description,
      'location' : group.preferredmeetingLoc,
      'preferredMeetingTimes' : calendar,
      'photo': photo,
      'lookingFor': group.skills.split(","),
      'weHave': wehave,
      'capacity': group.capacity,
      'vacancy': vacancy
    }
    return result
  
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

def getMember(id):
  members = []
  for group in Group.objects.all():
    if group.id == id:
      info = {
        "name" : group.owner.name
      }
      members.append(info)
  for groupMem in GroupMember.objects.all():
    if (groupMem.group.id == id and groupMem.status):
      info = {
        "name" : groupMem.member.name
      }
      members.append(info)
  return members

def getCalendar(id):
  events = []
  for event in Calendar.objects.all():
    if event.group.id == id:
      events.append(CalendarSerializer(event).data)
  return events

def getCalendarGroups(request, id, rid):
  groups = []
  student = getStudentJson(id)
  for group in Group.objects.all():
    if group.room.id == rid:
      groups.append(getGroupJson(group))
  sortedGroups = sortGroupByAvailabilities(groups, student)
  return JsonResponse(sortedGroups, safe=False)
  
def getRoomMembers(request, id, rid, gid):
  members = []
  room = Room.objects.get(id=rid)
  for member in room.members.all():
    matchedskills = getMatchedSkills(member, gid)
    if (checkGroupMember(member, room) and member.id != id):
      members.append({
        "name" : member.name,
        "id" : member.id,
        "bio": member.bio,
        "photo": json.dumps(str(member.photo)),
        "skills": matchedskills
      })
  return JsonResponse(members, safe=False)
          

def checkGroupMember(member, room):
  for memb in GroupMember.objects.all():
    if (memb.member == member and memb.group.room == room):
      return False
  for group in Group.objects.all():
    if (group.room == room and group.owner == member):
      return False
  return True

def getMatchedSkills(student, gid):
  group = Group.objects.get(id=gid)
  skills = group.skills.split(", ")
  courses=[]
  for course in student.courses.all():
    courses.append(course.name)
  matchedskills = lookingfor(skills, courses)
  return matchedskills

def getSkillsGroups(request, id, rid):
  groups = []
  student = Student.objects.get(id=id)
  for group in Group.objects.all():
    if group.room.id == rid:
      groups.append(getGroupJson(group))
  sortedGroups = sortGroupBySkills(groups, student)
  return JsonResponse(sortedGroups, safe=False)

def getOverallGroups(request, id, rid):
  groups = []
  student = getStudentJson(id)
  student2 = Student.objects.get(id=id)
  for group in Group.objects.all():
    if group.room.id == rid:
      groups.append(getGroupJson(group))
  sortedGroups = sortOverallGroups(groups, student, student2)
  return JsonResponse(sortedGroups, safe=False)
