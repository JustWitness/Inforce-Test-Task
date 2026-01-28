from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count
from .models import Menu
from menus.serializers import MenuSerializer, MenuVoteSerializer
from users.permissions import IsRestaurant, IsEmployee


# Create your views here.
class MenuAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsRestaurant]
    serializer_class = MenuSerializer

    def get(self, request, *args, **kwargs):
        menu = Menu.objects.filter(
            restaurant=request.user,
            date=timezone.localdate()
        ).first()

        if not menu:
            return Response({"detail": "No menu created for today."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(menu)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(restaurant=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvailableMenusAPIView(GenericAPIView):
    queryset = Menu.objects.filter(date=timezone.localdate())
    permission_classes = [IsAuthenticated, IsEmployee]
    serializer_class = MenuSerializer

    def get(self, request, *args, **kwargs):
        queryset = Menu.objects.filter(date=timezone.localdate())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuVoteAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsEmployee]
    serializer_class = MenuVoteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MenuResultsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsEmployee]
    serializer_class = MenuSerializer

    def get(self, request, *args, **kwargs):
        winner = Menu.objects.filter(
            date=timezone.localdate()
        ).annotate(total_votes=Count('votes')).order_by('-total_votes').first()

        if not winner:
            return Response("No menus today", status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(winner)
        return Response(serializer.data, status=status.HTTP_200_OK)
