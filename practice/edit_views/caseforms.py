from django import forms
from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _

from practice.models import Person, Case

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
        labels = dict(casenum = 'Case #',
                                 id = 'Internal Id',
                                 representationfee = 'Rep Fee',
                                 trialfee = 'Trial Fee',
                                 description = 'Description',
                                 initialpayment='Initial Pmt')

        widgets = dict(person= forms.HiddenInput, id= forms.HiddenInput)

