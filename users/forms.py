from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserCreateForm(UserCreationForm):
        class Meta:
            model = User
            fields = ('email', 'username', 'first_name', 'last_name', 'role')


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username')