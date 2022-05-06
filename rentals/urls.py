from django.urls import path

from rentals import views

app_name = 'rentals'

urlpatterns = [
    path('list/', views.ReservationListView.as_view(), name='list'),
]
