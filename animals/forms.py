from django import forms
from animals.models import Animal


class IndexForm(forms.Form):
    animals = forms.ModelChoiceField(queryset=Animal.objects.filter(deleted=False))


class ShowForm(forms.Form):
    animal_id = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    arrival_date = forms.DateField(widget=forms.DateInput(attrs={'readonly':'readonly'}))
    weight = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    height = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    spec_features = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
