from django.urls import path
from parking.views import *
app_name = 'parking'

urlpatterns = [
    path('park_view',park_view,name="park_view"),
    path('leave_view',leave_view,name="leave_view"),
    path('park_avail',parking_image),
    path('locate_car',locate_car),
]