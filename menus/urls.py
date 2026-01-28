from django.urls import path
from .views import *

urlpatterns = [
    path("menu/", MenuAPIView.as_view()),
    path("menu/available", AvailableMenusAPIView.as_view()),
    path("menu/vote/", MenuVoteAPIView.as_view()),
    path("menu/winner", MenuResultsAPIView.as_view()),
]