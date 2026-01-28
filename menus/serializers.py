from django.utils import timezone
from rest_framework import serializers
from .models import Menu, MenuItem, MenuVote


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price']

    def create(self, validated_data):
        return MenuItem.objects.create(**validated_data)


class MenuVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuVote
        fields = ['id', 'menu', 'employee', 'created_at']
        read_only_fields = ['employee']

    def create(self, validated_data):
        employee = self.context['request'].user

        return MenuVote.objects.create(employee=employee, **validated_data)

    def validate(self, data):
        employee = self.context['request'].user
        menu = data['menu']

        already_voted = MenuVote.objects.filter(menu__date=menu.date, employee=employee).exists()

        if already_voted:
            raise serializers.ValidationError("You already voted today")

        return data


class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)
    total_price = serializers.ReadOnlyField()
    vote_count = serializers.ReadOnlyField()

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'name', 'date', 'items', 'total_price', 'vote_count']
        read_only_fields = ['restaurant']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        menu = Menu.objects.create(**validated_data)

        for item_data in items_data:
            MenuItem.objects.create(menu=menu, **item_data)

        return menu

    def validate_date(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError("You can't create menu for a past date")
        return value
