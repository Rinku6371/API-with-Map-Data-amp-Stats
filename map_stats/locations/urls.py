from django.urls import path
from .views import LocationList, LocationStats

urlpatterns = [
    path('locations/', LocationList.as_view(), name='location-list'),
    path('locations/stats/', LocationStats.as_view(), name='location-stats'),
]

