from .models import Event
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'location', 'date', 'time', 'ticket_price', 'organizer']

    def get_organizer(self, obj):
        return obj.organizer.username if obj.organizer else None