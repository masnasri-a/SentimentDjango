
from django.forms import ModelForm
from .models import input_sentimen

class inputanForm(ModelForm):
    class Meta:
        model = input_sentimen
        fields = '__all__'
