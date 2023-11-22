import factory
from faker import Faker
import random
from tickets.models import Ticket, TicketType
from events.models import Event,EventTicketType
from accounts.models import Account

fake = Faker()

class TicketTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TicketType

    name = fake.name()
    
    
class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    event = Event.objects.get(id=34)
    customer = Account.objects.get(id=19)
    # event = list(Event.objects.all())[random.randint(1,Event.objects.count())]
    # customer =list(Account.objects.all())[random.randint(1,Account.objects.count())]
    ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
    price = random.randint(500, 1000)