from rest_framework import serializers
from .models import Photo,Event,EventTicketTypes,Ticket

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
    
    def to_representation(self, instance):
        if not instance.is_active:
            return None
        return super().to_representation(instance)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        
    def delete(self, instance):
        instance.is_active=False
        instance.save()
        
    def to_representation(self, instance):
        if not instance.is_active:
            return None
        return super().to_representation(instance)


class EventSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    tickets = serializers.SerializerMethodField()
    
    def get_tickets(self,obj):
        tickets = EventTicketTypes.objects.filter(event=obj)
        return TicketSerializer(tickets,many=True).data

    def get_photos(self, obj):
        photos = Photo.objects.filter(blogs=obj)
        return PhotoSerializer(photos, many=True, read_only=False).data
    
    def to_representation(self, instance):
        if not instance.is_active:
            return None
        return super().to_representation(instance)

    class Meta:
        model = Event
        fields = ['photos',]