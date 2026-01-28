from django.urls import path
from .views import MenuAPIView, AvailableMenusAPIView, MenuVoteAPIView, MenuResultsAPIView

urlpatterns = [
    path("menu/", MenuAPIView.as_view(), name="menu"),
    path("menu/available", AvailableMenusAPIView.as_view(), name="menu-available"),
    path("menu/vote/", MenuVoteAPIView.as_view(), name="menu-vote"),
    path("menu/winner", MenuResultsAPIView.as_view(), name="menu-winner"),
]
