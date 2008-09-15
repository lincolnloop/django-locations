from django import newforms as forms
from models import Location
        
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ('slug',)