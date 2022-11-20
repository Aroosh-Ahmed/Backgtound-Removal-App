from django.urls import path,include

from .views import removebgview

urlpatterns = [
    path("removebg", removebgview)
]