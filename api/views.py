import time
import tracemalloc
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import Account
from events_tickets.models import TicketType, Event, Ticket
import random
from django.core.mail import send_mail
from events_tickets.models import Ticket, Event
from accounts.models import Account
from datetime import datetime, timedelta

from Event_Management.settings import EMAIL_HOST_USER


# Create your views here.
@api_view(["GET"])
def create_sample_tickets(request):
    events = Event.objects.all()
    customers = Account.objects.all()
    ticket_types = TicketType.objects.all()

    # print(random.choice(events).id)
    # print(random.choice(customers).id)
    # print(random.choice(ticket_types).id)
    for ticket in range(100000):
        inst = Ticket(event=random.choice(events),customer = random.choice(customers),ticket_type = random.choice(ticket_types),price = random.randint(500,1000),is_active = True,archive=False )
        inst.save()
        # print(inst)
    # print(Ticket.objects.get(id=15).customer.email)
    return Response("hello")


@api_view(["GET"])
def create_notification(request):
    start_time = time.time()
    tracemalloc.start()
    tickets = (
        Ticket.objects.all()
        .values_list(
            "event",
            "event__name",
            "event__date",
            "event__time",
            "event__location",
            "customer__email",
            "customer__fname",
            "customer__lname",
        )
        .distinct()
    )
    data_dict = {}
    for ticket in tickets:
        if ticket[0] not in data_dict.keys():
            event = {
                "name": ticket[1],
                "date": ticket[2],
                "time": ticket[3],
                "location": ticket[4],
            }
            customer = {"email": ticket[5], "fname": ticket[6], "lname": ticket[7]}
            data_dict[ticket[0]] = [{"event": event, "customer": customer}]
        else:
            data_dict[ticket[0]].append({"event": event, "customer": customer})
    print(data_dict)
    for ticket_data in data_dict.values():
        for ticket in ticket_data:
            # print(ticket['event'],ticket['customer'])
            subject = f"Reminder for {ticket['event']['name']} Event"
            message = f"""
            Hello {ticket['customer']['fname'] +" "+ ticket['customer']['lname']}
            This is to remind you that you have booked a ticket for event {ticket['event']['name']}. The details are as follows :
            
            Event name : {ticket['event']['name']}
            Event Date : {ticket['event']['date']}
            Event time : {ticket['event']['time']}
            Event location : {ticket['event']['location']}
            
            This is a reminder email for the event mentioned above. Hope to see you on time. Have a great event.
            Thank you.
            """
    end_time = time.time()
    # tracemalloc.stop()
    print("execution time of custom dict = ",end_time-start_time)
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    # print("execution memory of custom dict = ",end_mem-start_mem)
    print(f"Current memory usage: {current_memory / (1024 * 1024):.2f} MB")
    print(f"Peak memory usage: {peak_memory / (1024 * 1024):.2f} MB")
    return Response("hello")

@api_view(["GET"])
def send_mail_to_attendees(request):
    start_time = time.time()
    tracemalloc.start()
    tickets = (
        Ticket.objects.filter(event__date__lte=datetime.now().date() + timedelta(1))
        .values_list("event_id", "customer_id")
        .distinct()
    )
    print(tickets)
    "(event_id,customer_id)"
    for i in tickets:
        event = Event.objects.get(id=i[0])
        attendee = Account.objects.get(id=i[1])
        subject = f"Reminder for {event.name} Event"
        message = f"""
        Hello {attendee.fname +" "+ attendee.lname}
        This is to remind you that you have booked a ticket for event {event.name}. The details are as follows :
        
        Event name : {event.name}
        Event Date : {event.date}
        Event time : {event.time}
        Event location : {event.location}
        
        This is a reminder email for the event mentioned above. Hope to see you on time. Have a great event.
        Thank you.
        """
    end_time = time.time()
    print("execution time of model = ", end_time-start_time)
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    # print("execution memory of custom dict = ",end_mem-start_mem)
    print(f"Current memory usage: {current_memory / (1024 * 1024):.2f} MB")
    print(f"Peak memory usage: {peak_memory / (1024 * 1024):.2f} MB")
    return Response("hello")