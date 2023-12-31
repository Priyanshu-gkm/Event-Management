from django.test import TestCase
from django.urls import reverse

from tickets.models import TicketType, Ticket
from tickets.model_factory import TicketTypeFactory, TicketFactory
from tickets.serializers import TicketTypeSerializer

from events.setup_data import get_setup_data
from events.models import Event, EventTicketType
from events.serializers import EventSerializer
from events.model_factory import EventFactory

from accounts.models import Account

from faker import Faker
import random
import factory

fake = Faker()


class TicketTypeLCViews(TestCase):
    def setUp(self):
        for k, v in get_setup_data().items():
            setattr(self, k, v)

    def test_CreateNewTicketType_admin_success(self):
        ticket_data = factory.build(dict, FACTORY_CLASS=TicketTypeFactory)
        response = self.client.post(
            reverse("LC-ticket-type"),
            data=TicketTypeSerializer(data=ticket_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_CreateNewTicketType_organizer_success(self):
        ticket_data = factory.build(dict, FACTORY_CLASS=TicketTypeFactory)
        response = self.client.post(
            reverse("LC-ticket-type"),
            data=TicketTypeSerializer(data=ticket_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_CreateNewTicketType_attendee_fail(self):
        ticket_data = factory.build(dict, FACTORY_CLASS=TicketTypeFactory)
        response = self.client.post(
            reverse("LC-ticket-type"),
            data=TicketTypeSerializer(data=ticket_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_ListTicketType_admin_success(self):
        response = self.client.get(
            reverse("LC-ticket-type"), HTTP_AUTHORIZATION=f"Token {self.admin_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_ListTicketType_organizer_success(self):
        response = self.client.get(
            reverse("LC-ticket-type"),
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_ListTicketType_attendee_fail(self):
        response = self.client.get(
            reverse("LC-ticket-type"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}"
        )
        self.assertEqual(response.status_code, 403)


class TicketTypeRUDViews(TestCase):
    def setUp(self):
        for k, v in get_setup_data().items():
            setattr(self, k, v)

        self.ticket_type_id = []
        for _ in range(3):
            TicketTypeFactory()
            self.ticket_type_id.append(TicketType.objects.latest("id").__dict__["id"])

        self.data = TicketType.objects.get(
            id=random.choice(self.ticket_type_id)
        ).__dict__
        self.data["name"] = fake.name()
        del self.data["_state"]

    def test_TicketType_Retrieve_admin_success(self):
        response = self.client.get(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketType_Retrieve_organizer_fail(self):
        response = self.client.get(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketType_Retrieve_attendee_fail(self):
        response = self.client.get(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketType_Update_admin_success(self):
        response = self.client.patch(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketType_Update_organizer_fail(self):
        response = self.client.patch(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketType_Update_attendee_fail(self):
        response = self.client.patch(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketType_Delete_admin_success(self):
        response = self.client.delete(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 204)

    def test_TicketType_Delete_organizer_fail(self):
        response = self.client.delete(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketType_Delete_attendee_fail(self):
        response = self.client.delete(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)


class TicketLCViews(TestCase):
    @classmethod
    def setUpTestData(self):
        for k, v in get_setup_data().items():
            setattr(self, k, v)
        for iter in range(3):
            TicketTypeFactory()

        for iter in range(3):
            ticks = list(TicketType.objects.values_list("pk", flat=True))
            tickets = [
                {
                    "ticket_type": ticks[_],
                    "price": fake.pyint(min_value=100, max_value=9999),
                    "quantity": fake.pyint(min_value=10, max_value=100),
                }
                for _ in range(1, 3)
            ]

            photos = [fake.url() for i in range(2)]

            event_data = factory.build(dict, FACTORY_CLASS=EventFactory)
            event_data["tickets"] = tickets
            event_data["photos"] = photos
            event_data["created_by"] = random.choice(
                list(Account.objects.values_list("pk", flat=True))
            )
            self.client.post(
                reverse("LC-event"),
                data=EventSerializer(data=event_data).initial_data,
                content_type="application/json",
                HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
            ).json()

        for iter in range(1, 4):
            event = list(Event.objects.all())[
                random.randint(1, Event.objects.count() - 1)
            ]
            customer = Account.objects.first()
            ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
            TicketFactory(event=event, customer=customer, ticket_type=ticket_type)

        event = list(Event.objects.all())[random.randint(1, Event.objects.count() - 1)]
        ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
        self.ticket_create_data = {
            "event": event.id,
            "tickets": [{"type": ticket_type.id, "quantity": 2}],
        }

    def test_TicketList_admin_success(self):
        response = self.client.get(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.admin_token}"
        )
        self.assertTrue(
            Ticket.objects.count() == len(response.json()),
            msg="equal number of objects",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketList_organizer_success(self):
        response = self.client.get(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.organizer_token}"
        )
        response_ids = set([i["event"] for i in response.json()])
        created_by_ids = set(
            [Event.objects.get(id=i).created_by.id for i in response_ids]
        )
        self.assertTrue(len(created_by_ids) == 1)
        self.assertTrue(self.organizer_id in created_by_ids)
        self.assertFalse(self.admin_id in created_by_ids)
        self.assertFalse(self.attendee_id in created_by_ids)
        self.assertEqual(response.status_code, 200)

    def test_TicketList_attendee_success(self):
        response = self.client.get(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}"
        )
        response_ids = set([i["customer"] for i in response.json()])
        self.assertTrue(len(response_ids) == 1)
        self.assertTrue(self.attendee_id in response_ids)
        self.assertFalse(self.admin_id in response_ids)
        self.assertFalse(self.organizer_id in response_ids)
        self.assertEqual(response.status_code, 200)

    def test_TicketCreate_admin_success(self):
        response = self.client.post(
            reverse("LC-ticket"),
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
            data=self.ticket_create_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_TicketCreate_organizer_success(self):
        response = self.client.post(
            reverse("LC-ticket"),
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
            data=self.ticket_create_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_TicketCreate_attendee_success(self):
        response = self.client.post(
            reverse("LC-ticket"),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
            data=self.ticket_create_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_TicketCreate_attendee_fail_event_does_not_exist(self):
        ticket_data = self.ticket_create_data
        ticket_data["event"] = random.randint(4000, 5000)
        try:
            response = self.client.post(
                reverse("LC-ticket"),
                HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
                data=ticket_data,
                content_type="application/json",
            )
        except Exception as e:
            self.assertEqual("Event matching query does not exist.", str(e))

    def test_TicketCreate_attendee_fail_event_inactive(self):
        inst = Event.objects.first()
        inst.is_active = False
        inst.save()
        self.ticket_create_data["event"] = inst.id
        response = self.client.post(
            reverse("LC-ticket"),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
            data=self.ticket_create_data,
            content_type="application/json",
        )
        self.assertIn("Invalid", str(response.json()))
        self.assertEqual(response.status_code, 400)

    def test_TicketCreate_attendee_fail_event_active_ticket_not_linked(self):
        self.ticket_create_data["tickets"][0]["type"] = random.randint(1000, 9999)
        response = self.client.post(
            reverse("LC-ticket"),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
            data=self.ticket_create_data,
            content_type="application/json",
        )
        self.assertIn("matching query does not exist.", str(response.json()))
        self.assertEqual(response.status_code, 400)


class TicketRUDViews(TestCase):
    @classmethod
    def setUpTestData(self):
        for k, v in get_setup_data().items():
            setattr(self, k, v)
        for iter in range(3):
            TicketTypeFactory()

        for iter in range(3):
            ticks = list(TicketType.objects.values_list("pk", flat=True))
            tickets = [
                {
                    "ticket_type": ticks[_],
                    "price": fake.pyint(min_value=100, max_value=9999),
                    "quantity": fake.pyint(min_value=10, max_value=100),
                }
                for _ in range(1, 3)
            ]

            photos = [fake.url() for i in range(2)]

            event_data = factory.build(dict, FACTORY_CLASS=EventFactory)
            event_data["tickets"] = tickets
            event_data["photos"] = photos
            event_data["created_by"] = random.choice(
                list(Account.objects.values_list("pk", flat=True))
            )
            self.client.post(
                reverse("LC-event"),
                data=EventSerializer(data=event_data).initial_data,
                content_type="application/json",
                HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
            ).json()

        for iter in range(1, 4):
            event = list(Event.objects.all())[
                random.randint(1, Event.objects.count() - 1)
            ]
            customer = Account.objects.first()
            ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
            TicketFactory(event=event, customer=customer, ticket_type=ticket_type)

        event = list(Event.objects.all())[random.randint(1, Event.objects.count() - 1)]
        ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
        self.ticket_create_data = {
            "event": event.id,
            "tickets": [{"type": ticket_type.id, "quantity": 2}],
        }

    def setUp(self):
        tickets = list(Ticket.objects.all())
        self.ticket = random.choice(tickets)

    def test_TicketRetrieve_admin_success(self):
        response = self.client.get(
            reverse("RUD-ticket", args=[self.ticket.id]),
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketRetrieve_attendee_success(self):
        event = list(Event.objects.all())[random.randint(1, Event.objects.count() - 1)]
        customer = self.attendee_user
        ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
        ticket = TicketFactory(event=event, customer=customer, ticket_type=ticket_type)
        response = self.client.get(
            reverse("RUD-ticket", args=[ticket.id]),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketRetrieve_attendee_fail(self):
        att_user = Account.objects.create_user(
            email="attendeeTest1@gmail.com",
            username="attendeeTest1",
            password="Test@Abcd",
            fname="att3",
            lname="dee3",
            gender="Female",
            role="ATTENDEE",
        )
        attendee_data = {"username": "attendeeTest1", "password": "Test@Abcd"}
        response = self.client.post(
            path=reverse("user_login"),
            data=attendee_data,
            content_type="application/json",
        )
        attendee_token = response.json()["token"]
        response = self.client.get(
            reverse("RUD-ticket", args=[self.ticket.id]),
            HTTP_AUTHORIZATION=f"Token {attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketRetrieve_organizer_success(self):
        response = self.client.get(
            reverse("RUD-ticket", args=[self.ticket.id]),
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketRetrieve_organizer_fail(self):
        org_user = Account.objects.create_user(
            email="orgTest2@gmail.com",
            username="orgTest2",
            password="Test@Abcd",
            fname="att3",
            lname="dee3",
            gender="Female",
            role="ORGANIZER",
        )
        org_data = {"username": "orgTest2", "password": "Test@Abcd"}
        response = self.client.post(
            path=reverse("user_login"), data=org_data, content_type="application/json"
        )
        org_token = response.json()["token"]
        response = self.client.get(
            reverse("RUD-ticket", args=[self.ticket.id]),
            HTTP_AUTHORIZATION=f"Token {org_token}",
        )
        self.assertEqual(response.status_code, 403)
