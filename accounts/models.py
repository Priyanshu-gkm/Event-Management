from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        ATTENDEE = "ATTENDEE", "Attendee"
        ORGANIZER = "ORGANIZER", "Organizer"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            if "role" in kwargs.keys():
                self.role = kwargs['role']
            else:
                self.role = self.base_role
            return super().save(*args, **kwargs)


class AttendeeManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.ATTENDEE)


class Attendee(User):

    base_role = User.Role.ATTENDEE

    attendee = AttendeeManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Attendee"


@receiver(post_save, sender=Attendee)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "ATTENDEE":
        AttendeeProfile.objects.create(user=instance)


class AttendeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Attendee_id = models.IntegerField(null=True, blank=True)


class OrganizerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.ORGANIZER)


class Organizer(User):

    base_role = User.Role.ORGANIZER

    organizer = OrganizerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for organizers"


class OrganizerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organizer_id = models.IntegerField(null=True, blank=True)


@receiver(post_save, sender=Organizer)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "ORGANIZER":
       OrganizerProfile.objects.create(user=instance)