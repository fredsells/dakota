from django import forms
from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _

from practice.models import Person, Case

class NewCaseForm(forms.ModelForm):

    class Meta:
        model = Case
        readonly_fields = ('person',)
        fields = ['person',  'casenum', 'representationfee', 'trialfee', 'description', 'initialpayment',
                  'begindate']
        labels = dict(casenum = 'Case #',
                                 id = 'Internal Id',
                                 representationfee = 'Rep Fee',
                                 trialfee = 'Trial Fee',
                                 description = 'Description',
                                 initialpayment='Initial Pmt')

        widgets = dict(person=forms.HiddenInput,
                       begindate=forms.DateInput(attrs={'class': 'datepicker'})

                       )

class CaseForm(forms.ModelForm):

    class Meta:
        model = Case
        fields = ['id', 'casenum', 'representationfee', 'trialfee', 'description', 'initialpayment',
                  'begindate', 'enddate']
        labels = dict(casenum = 'Case #',
                                 id = 'Internal Id',
                                 representationfee = 'Rep Fee',
                                 trialfee = 'Trial Fee',
                                 description = 'Description',
                                 initialpayment='Initial Pmt')

        widgets = dict(person_id=forms.HiddenInput,
                       id=forms.HiddenInput,
                       begindate=forms.DateInput(attrs={'class': 'datepicker'}),
                       enddate=forms.DateInput(attrs={'class': 'datepicker'})
                       )

