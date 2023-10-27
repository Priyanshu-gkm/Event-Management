from django.db import models
from events_tickets.custom_validators import validate_date_greater_than_today
from Event_Management.settings import AUTH_USER_MODEL
from django.db.models.signals import post_delete
from django.dispatch import receiver

class TicketTypes(models.Model):
    name = models.CharField(max_length=20,null=False,blank=False)
    created_by = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True,verbose_name="active")
    
    def delete(self, *args, **kwargs):
        # Custom delete logic
        self.is_active=False
        self.save()
    

class Event(models.Model):
    name = models.CharField(verbose_name="name",max_length=100)
    date = models.DateField(verbose_name="date",blank=False,null=False,validators=[validate_date_greater_than_today])
    time = models.TimeField(verbose_name="time",blank=False,null=False)
    location = models.CharField(verbose_name="location",blank=False,null=False,max_length=255)
    description = models.TextField(verbose_name="description")
    created_by = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    # tickets =  serializers.SerialzerMethodField
    # images = multiple images saving thing
    is_active = models.BooleanField(default=True,verbose_name="active")
    
    def delete(self, *args, **kwargs):
        # Custom delete logic
        self.is_active=False
        self.save()
        

class EventTicketTypes(models.Model):
    event = models.ForeignKey(Event,verbose_name="event",on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketTypes,verbose_name="ticket",on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name="price",max_digits=7,decimal_places=2)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True,verbose_name="active")
    

@receiver(post_delete, sender=Event)
def update_event_ticket_types(sender, instance, **kwargs):
    if not instance.is_active:
        # When the Event is declared inactive, set related EventTicketType instances to inactive
        EventTicketTypes.objects.filter(event=instance).update(is_active=False)
    
    
    
class Photo(models.Model):
    event = models.ForeignKey(Event, related_name='event_img',on_delete=models.CASCADE)
    image = models.TextField()
    
    
class Ticket(models.Model):
    event = models.ForeignKey(Event)
    customer = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketTypes,verbose_name="ticket")
    price = models.DecimalField(max_digits=7,decimal_places=2)
    is_active = models.BooleanField(default=True,verbose_name="active")
        
        
@receiver(post_delete, sender=Event)
def update_ticket(sender, instance, **kwargs):
    if not instance.is_active:
        # When the Event is declared inactive, set related EventTicketType instances to inactive
        Ticket.objects.filter(event=instance).update(is_active=False)
    