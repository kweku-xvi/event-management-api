from accounts.serializers import UserInfoSerializer
from .models import Event, Registration
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'location', 'date', 'time', 'ticket_price', 'organizer']

    def get_organizer(self, obj):
        return obj.organizer.username if obj.organizer else None


class EventRegistrationSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()
    user = UserInfoSerializer()

    class Meta:
        model = Registration
        fields = ['event', 'user', 'date_registered']

    def get_event(self, obj):
        return obj.event.name if obj.event else None