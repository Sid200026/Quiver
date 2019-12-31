from django.forms import ModelForm
from .models import Beaver

class BeaverForm(ModelForm):
    class Meta:
        model = Beaver
        exclude = ['user', 'friends']
