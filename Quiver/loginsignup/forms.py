from django.forms import ModelForm
from .models import Beaver


class BeaverForm(ModelForm):
    class Meta:
        model = Beaver
        exclude = ['user', 'friends']

    def checkProfile(self, request):
        if self.is_valid():
            beaver = self.save(commit=False)
            beaver.user = request.user
            beaver.save()
            return True
        return False
