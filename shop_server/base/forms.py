from django.forms import ModelForm
from .models import Item
from .models import User


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__' #['name', '']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password'] #['name', '']


