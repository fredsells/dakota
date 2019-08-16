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
        fields = '__all__'
        widgets = {
            'dateposted': forms.DateInput(attrs={'class': 'datepicker'})
        }




    # personid = forms.IntegerField()
    # dateposted = forms.DateField()
    # description = forms.CharField( max_length=60)
    # #type = forms.ChoiceField(choices=TransactionType.objects.all())
    # amount = forms.DecimalField(max_digits=8)



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'


