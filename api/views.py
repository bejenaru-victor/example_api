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


@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'GET': {
			'Future event list': '/event-list/',
			'User event list': '/user-event-list/{user_id}/',
		},
		'POST': {
			'Create event': 'create-event/'
		},
		'PUT': {
			'Update event date': '/update-event-date/{event_id}/',
		},
		'DELETE': {
			'Delete event': 'delete-event/{event_id}/'
		},
	}
	return Response(api_urls)


@api_view(['GET'])
def eventList(request):
	events = Event.objects.filter(starting_at__gt=datetime.now())
	serializer = EventSerializer(events, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def userEventList(request, user):
	try:
		user = User.objects.get(pk=user)
	except:
		raise NotFound()

	events = Event.objects.filter(attendants__in=[user,])
	serializer = EventSerializer(events, many=True)
	return Response(serializer.data)


@api_view(['PUT'])
def updateEventDate(request, event):
	try:
		event = Event.objects.get(pk=event)
	except:
		raise NotFound()

	starting_at = request.data.get('starting_at', None)
	password = request.data.get('password', None)
	if starting_at and ((event.password and password and check_password(password, event.password)) or not event.password):
		serializer = EventSerializer(instance=event, data={ 'starting_at': starting_at}, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)
	else:
		raise NotFound(detail='Missing starting_at argument or invalid password', code=400)


@api_view(['POST'])
def createEvent(request):
	serializer = EventSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	return Response(serializer.errors)


@api_view(['DELETE'])
def deleteEvent(request, event):
	try:
		event = Event.objects.get(pk=event)
	except:
		raise NotFound()

	password = request.data.get('password', None)
	if (event.password and password and check_password(password, event.password)) or not event.password:
		event.delete()	
		return Response({'details': 'Event deleted successfully'})
	else:
		raise NotFound(detail='Invalid password')
	