from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt


def lobby(request):
    return render(request, "base/lobby.html")


def room(request):
    return render(request, "base/room.html")


def getToken(request):
    appId = "fc3b80f1c357472eb1de68635545cff5"
    appCertificate = "ce99b25099a74b279d4e53a0bae31928" 
    channelName = request.GET.get("channel")
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({"token": token, "uid": uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)




def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(name=data['name'],uid=data['UID'],room_name=data['room_name'])
    member.delete()
    return JsonResponse('Member deleted', safe=False)