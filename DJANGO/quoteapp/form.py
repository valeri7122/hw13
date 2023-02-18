from django.forms import ModelForm, CharField, TextInput
from .models import Quote, Author


class QuoteForm(ModelForm):
    quote = CharField(max_length=2000, required=True, widget=TextInput())    

    class Meta:
        model = Quote
        fields = ['quote','author']
        exclude = ['tags']


class AuthorForm(ModelForm):
    fullname = CharField(max_length=50, required=True, widget=TextInput())
    born_date = CharField(max_length=150, required=True, widget=TextInput())
    born_location = CharField(max_length=100, required=True, widget=TextInput())      
    description = CharField(max_length=5000, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
