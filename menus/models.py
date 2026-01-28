from django.db import models
from django.conf import settings
from django.db.models import Sum

from users.enums import UserRole
from users.models import User


# Create your models here.
class Menu(models.Model):
    restaurant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='menus',
        on_delete=models.CASCADE,
        limit_choices_to={'role': UserRole.RESTAURANT},
    )
    name = models.CharField(max_length=200)
    date = models.DateField()

    @property
    def total_price(self):
        result = self.items.aggregate(total=Sum('price'))
        return result['total'] or 0.0

    @property
    def vote_count(self):
        return self.votes.count()

    class Meta:
        unique_together = ('restaurant', 'date')
        ordering = ('-date',)

    def __str__(self):
        return f'{self.restaurant} - {self.date}'


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='items',
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.menu} - {self.name}'


class MenuVote(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='votes',
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='votes',
        limit_choices_to={'role': UserRole.EMPLOYEE},
    )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'created_at')

    def __str__(self):
        return f'{self.employee.username} - {self.created_at}'
