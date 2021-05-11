from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound as DRFNotFound

from .serializers import EventSerializer

from events.models import Event

import json


def NotFound(detail=None, code=404):
    if not detail:
        detail = "Error 404, page not found"
    return DRFNotFound(detail=detail, code=code)


def eventPasswordValidation(event, password):
    if event.password:
        if not password:
            raise NotFound(detail="Missing password argument", code=400)
        elif not check_password(password, event.password):
            raise NotFound(detail="Invalid password", code=403)


@api_view(["GET"])
def apiOverview(request):
    api_urls = {
        "GET": {
            "Future event list": "/event-list/",
            "User event list": "/user-event-list/{user_id}/",
        },
        "POST": {"Create event": "create-event/"},
        "PUT": {
            "Update event date": "/update-event-date/{event_id}/",
        },
        "DELETE": {"Delete event": "delete-event/{event_id}/"},
    }
    return Response(api_urls)


@api_view(["GET"])
def eventList(request):
    events = Event.objects.filter(starting_at__gt=datetime.now())
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def userEventList(request, user):
    try:
        user = User.objects.get(pk=user)
    except:
        raise NotFound()

    events = Event.objects.filter(
        attendants__in=[
            user,
        ]
    )
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(["PUT", "DELETE"])
def updateEvent(request, event):
    try:
        event = Event.objects.get(pk=event)
    except:
        raise NotFound()

    password = request.data.get("password", None)
    eventPasswordValidation(event, password)
    if request.method == "PUT":
        starting_at = request.data.get("starting_at", None)
        if not starting_at:
            raise NotFound(detail="Missing starting_at argument", code=400)
        serializer = EventSerializer(
            instance=event, data={"starting_at": starting_at}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    event.delete()
    return Response({"details": "Event deleted successfully"})


@api_view(["POST"])
def createEvent(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)
