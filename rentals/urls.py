from django.urls import path

from rentals import views

app_name = 'rentals'

urlpatterns = [
    path('list/', views.ReservationListView.as_view(), name='reservation_list'),
    path('create-rental/', views.RentalCreateView.as_view(), name='rental_create'),
    path('create-reservation/', views.ReservationCreateView.as_view(), name='reservation_create'),
]
