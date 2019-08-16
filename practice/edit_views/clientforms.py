
from django import forms
from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _

from practice.models import Person, Case


class NewPersonForm(forms.ModelForm):
    #size = forms.ModelChoiceField(queryset=Case.objects, empty_label=None, widget=forms.CheckBoxSelectMultiple)
    class Meta:
        model = Person
        fields = ['lastname', 'firstname', 'addr1'] #, 'addr2', 'city', 'state', 'zip', 'email']
        exclude = ('id',)
        labels = dict(lastname='Last Name',
                                 firstname='First Name',
                                 addr1='Address Line 1'
                                 )

class PersonForm(forms.ModelForm):
    #size = forms.ModelChoiceField(queryset=Case.objects, empty_label=None, widget=forms.CheckBoxSelectMultiple)
    class Meta:
        model = Person
        fields = '__all__'#  '['lastname', 'firstname']#, 'addr1', 'addr2', 'city', 'state', 'zip', 'email']
        labels = dict(lastname='Last Name',
                                 firstname='First Name',
                                 #addr1='Address Line 1'
                                 )
        widgets = dict(id=forms.HiddenInput)

