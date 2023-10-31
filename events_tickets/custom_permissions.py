from rest_framework import permissions

class IsOrganizer(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user has a 'organizer' role

        return bool(request.user and request.user.role == 'ORGANIZER')
    
class isAttendee(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role=="ATTENDEE")