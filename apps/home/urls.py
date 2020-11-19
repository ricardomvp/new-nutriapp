from django.urls import path

from apps.home.views import *
urlpatterns = [
    path('page/<str:page>', home, name='home'),
    path('card/<str:id>', card, name='card')
]
