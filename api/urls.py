from django.urls import path

from . import views

urlpatterns = [
    path("", views.apiOverview, name="api-overview"),
    path("event-list/", views.eventList, name="event-list"),
    path("user-event-list/<int:user>/", views.userEventList, name="user-event-list"),
    path(
        "update-event-date/<int:event>/",
        views.updateEvent,
        name="update-event-date",
    ),
    path("create-event/", views.createEvent, name="create-event"),
    path("delete-event/<int:event>/", views.updateEvent, name="delete-event"),
]
