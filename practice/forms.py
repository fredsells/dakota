'''
Created on Jul 9, 2019

@author: fsells
'''
from django import forms
from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _

from .models import Person, Case

def make_dictionary(**kwargs): return kwargs



class NewPersonForm(forms.ModelForm):
    #size = forms.ModelChoiceField(queryset=Case.objects, empty_label=None, widget=forms.CheckBoxSelectMultiple)
    class Meta:
        model = Person
        fields = ['lastname', 'firstname', 'addr1'] #, 'addr2', 'city', 'state', 'zip', 'email']
        exclude = ('id',)
        labels = make_dictionary(lastname='Last Name',
                                 firstname='First Name',
                                 addr1='Address Line 1'
                                 )

class PersonForm(forms.ModelForm):
    #size = forms.ModelChoiceField(queryset=Case.objects, empty_label=None, widget=forms.CheckBoxSelectMultiple)
    class Meta:
        model = Person
        fields = '__all__'#  '['lastname', 'firstname']#, 'addr1', 'addr2', 'city', 'state', 'zip', 'email']
        labels = make_dictionary(lastname='Last Name',
                                 firstname='First Name',
                                 #addr1='Address Line 1'
                                 )
        widgets = make_dictionary(id=forms.HiddenInput)

        



class NewCaseForm(forms.Form):
        personid = forms.IntegerField()
        casenum = forms.CharField(max_length=14 )
        description = forms.CharField(max_length=60)
        representationfee = forms.DecimalField(max_digits=8)
        trialfee = forms.DecimalField(max_digits=8)
        initialpayment = forms.DecimalField(max_digits=8)
        begindate = forms.DateField()


        
class CaseForm(forms.ModelForm):

    class Meta:
        model = Case
        fields = ['person', 'id', 'casenum', 'representationfee', 'trialfee', 'description', 'initialpayment',
                  'begindate', 'enddate']
        labels = make_dictionary(casenum = 'Case #',
                                 id = 'Internal Id',
                                 representationfee = 'Rep Fee',
                                 trialfee = 'Trial Fee',
                                 description = 'Description',
                                 initialpayment='Initial Pmt')

        widgets = make_dictionary(person= forms.HiddenInput, id= forms.HiddenInput)

