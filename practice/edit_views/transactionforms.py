from django import forms
from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _
import datetime
from practice.models import Person, Case, Transaction, TransactionType

class NewTransactionForm(forms.ModelForm):
    # clientid = forms.IntegerField()
    # def __init__(self, *args, **kwargs):
    #     print ('xxxxxxxxxxxxxxxxxxxxxxxx', args, kwargs)
    #     super(NewTransactionForm, self).__init__(*args, **kwargs)
    #     initial = kwargs.get('initial', None)
    #     if initial:
    #         person = initial.get('person', 0)
    #         self.fields['clientid'].initial = person.id
    #     else:
    #         print('xxxxxxxxxxxxxxxxxxxx initial missing')


    class Meta:
        model = Transaction
        fields = ['person', 'dateposted', 'transtype', 'description', 'amount']


        #widgets = dict(person=forms.HiddenInput, id=forms.HiddenInput)
        widgets = dict(dateposted=forms.DateInput(attrs={'class': 'datepicker'}),
                       #person=forms.HiddenInput,
                       #id=forms.HiddenInput
                       )




class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['id',  'dateposted', 'transtype', 'description', 'amount']
        labels = dict(casenum='Transaction Type',
                      id='Internal Id',
                      )
        widgets = {
            'dateposted': forms.DateInput(attrs={'class': 'datepicker'}),
            'id': forms.HiddenInput,
        }


