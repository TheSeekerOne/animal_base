from django import forms
from animals.models import Animal


class IndexForm(forms.Form):
    animals = forms.ModelChoiceField(queryset=Animal.objects.all())


class ShowForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    arrival_date = forms.DateField(widget=forms.DateInput(attrs={'readonly':'readonly'}))
    weight = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    height = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    spec_features = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))


class AddForm(forms.Form):
    name = forms.CharField(max_length=64, required=True, widget=forms.TextInput)
    age = forms.IntegerField(min_value=1, max_value=150, required=True)
    arrival_date = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"), required=False)
    weight = forms.FloatField(min_value=1, max_value=9999, required=True)
    height = forms.FloatField(min_value=1, max_value=99, required=True)
    spec_features = forms.CharField(widget=forms.Textarea)
