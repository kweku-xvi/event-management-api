from .models import Event, Registration
from .serializers import EventSerializer, EventRegistrationSerializer
from accounts.permissions import IsVerified
from datetime import timedelta
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


def get_event(event_id):
    try:
        event = Event.objects.get(id=event_id)
        return event
    except Event.DoesNotExist:
        return Response(
            {
                'success':False,
                'message':'Event does not exist'
            }, status=status.HTTP_400_BAD_REQUEST
        )


def get_timeframe(days):
    now = timezone.now()
    time_frame = now + timedelta(days=days)
    events = Event.objects.filter(date__gte=now.date(), date__lte=time_frame.date())

    return events


@api_view(['POST'])
@permission_classes([IsVerified])
def create_event_view(request):
    if request.method == 'POST':
        user = request.user
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(organizer=user)

            return Response(
                {
                    'success':True,
                    'data':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'data':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_event_details_view(request, event_id):
    if request.method == 'GET':
        event = get_event(event_id=event_id)

        serializer = EventSerializer(event)

        return Response(
            {
                'success':True,
                'event':serializer.data
            }, status=status.HTTP_200_OK
        )

@api_view(['GET'])
def get_all_events_view(request):
    if request.method == 'GET':
        events = Event.objects.all()

        serializer = EventSerializer(events, many=True)

        return Response(
            {
                'success':True,
                'event':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsVerified])
def update_event_details_view(request, event_id):
    if request.method == 'PUT' or request.method == 'PATCH':
        user = request.user
        event = get_event(event_id=event_id)

        if user != event.organizer and user.is_staff == False:
            return Response(
                {
                    'success':False,
                    'message':'You do not have the permission to perform this action. Only event admins can update event details'
                }, status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = EventSerializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'success':True,
                    'message':'Event details has been successfully updated',
                    'event':serializer.data
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                'success':False,
                'message':'Event update failed',
                'errors':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
@permission_classes([IsVerified])
def delete_event_view(request, event_id):
    if request.method == 'DELETE':
        user = request.user
        event = get_event(event_id=event_id)

        if user != event.organizer and user.is_staff == False:
            return Response(
                {
                    'success':False,
                    'message':'You do not have the permission to perform this action. Only event admins can delete event'
                }, status=status.HTTP_403_FORBIDDEN
            )

        event.delete()
        return Response(
            {
                'success':True,
                'message':'Event has been successfully deleted!'
            }, status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
def search_events_view(request): # search events by name, location or organizer
    if request.method == 'GET':
        query = request.query_params.get('query')

        if not query:
            return Response(
                {
                    'success':False,
                    'message':'Please provide a search query'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        events = Event.objects.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(organizer__username__icontains=query)
        )

        serializer = EventSerializer(events, many=True)

        return Response(
            {
                'success':True,
                'message':'Here are your search results',
                'events':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
def filter_events_view(request): # filters events by name, location or event admin 
    if request.method == 'GET':
        events = Event.objects.all()

        name = request.query_params.get('name')
        location = request.query_params.get('location')
        organizer = request.query_params.get('organizer')

        if not name and not location and not organizer:
            return Response(
                {
                    'success':False,
                    'message':'Please provide a filter query'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        if name:
            events = events.filter(name__iexact=name)
        if location:
            events = events.filter(location__iexact=location)
        if organizer:
            events = events.filter(organizer__username__iexact=organizer)

        serializer = EventSerializer(events, many=True)

        return Response(
            {
                'success':True,
                'message':'Here are the events after filtering',
                'events':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
def events_within_next_7_days_view(request):
    if request.method == 'GET':
        events = get_timeframe(days=7)

        serializer = EventSerializer(events, many=True)

        return Response(
            {
                'success':True,
                'message':'Results for events within the next week',
                'events':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
def events_within_next_month_view(request):
    if request.method == 'GET':
        events = get_timeframe(days=30)

        serializer = EventSerializer(events, many=True)

        return Response(
            {
                'success':True,
                'message':'Results for events within the next week',
                'events':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([IsVerified])
def register_for_event_view(request, event_id):
    if request.method == 'POST':
        now = timezone.now()
        user = request.user
        event = get_event(event_id=event_id)

        registration = Registration.objects.create(user=user, event=event)

        serializer = EventRegistrationSerializer(registration)

        return Response(
            {
                'success':True, 
                'message':f"You have successfully registered for '{event.name}'",
                'details':serializer.data
            }, status=status.HTTP_201_CREATED
        )

# todo : ticketing system