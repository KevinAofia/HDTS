from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . models import Requester

class CreateBasicUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

class CreateRequester(ModelForm):
    class Meta:
        model = Requester
        fields = [
            'firstName',
            'lastName',
            'email',
            'username',
            'password',
            'directSupervisorEmail',
            'branchChiefEmail'
        ]