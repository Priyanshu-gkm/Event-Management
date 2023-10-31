from django.test import TestCase , Client
from django.urls import reverse
from events_tickets.models import Event,EventTicketTypes,Ticket,TicketTypes,Photo
# Create your tests here.


class EventChecks(TestCase):
    def setUP(self):
        self.client = Client()
        
    
    def test_CreateNewEvent_name_missing(self):
        self.assertTrue(1==2)
    
    def test_CreateNewEvent_date_missing(self):
        self.assertTrue(1==2)
    
    def test_CreateNewEvent_time_missing(self):
        self.assertTrue(1==2)
    
    def test_CreateNewEvent_location_missing(self):
        self.assertTrue(1==2)
    
    def test_CreateNewEvent_description_missing(self):
        self.assertTrue(1==2)
    
    def test_UploadImage(self):
        self.assertTrue(1==2)
    
    
    def test_CreateNewEvent(self):
        self.assertTrue(1==2)
    
    
    def test_CreateNewEventTicketType(self):
        self.assertTrue(1==2)
    
    
    
class TicketViews(TestCase):
    
    def test_CreateTicketType(self):
        self.assertTrue(1==2)
    
    def test_ViewTicketTypes(self):
        self.assertTrue(1==2)
    
    
    def test_CreateNewTicket_purchase_invalid_event(self):
        self.assertTrue(1==2)
    
    
    def test_CreateNewTicket_purchase_invalid_user(self):
        self.assertTrue(1==2)
    
    
    def test_CreateNewTicket_purchase_invalid_TicketType(self):
        self.assertTrue(1==2)
    
    
    def test_CreateNewTicket_purchase_invalid_price(self):
        self.assertTrue(1==2)
    

class EventTicketChecks(TestCase):
    
    def test_EventTypeExists(self):
        self.assertTrue(1==2)
    
    def test_TicketTypeExists(self):
        self.assertTrue(1==2)
    
    