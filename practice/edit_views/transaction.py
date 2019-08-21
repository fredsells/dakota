from __future__ import absolute_import

import datetime, random


from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
#################################from django.db.models import Count
from django.db.models.functions import Lower
from django.http import JsonResponse
#from rest_framework import viewsets
from django.contrib.auth.decorators import permission_required


from practice.models import Person, Case, Transaction, TransactionType

from .transactionforms import NewTransactionForm, TransactionForm

ID='id'

def newtransaction(request):
    note = 'new transaction note'
    if request.method == 'GET':
        clientid = request.GET['clientid']  # required; throw exception if missing
        person = Person.objects.get(pk=int(clientid))  # might have to change to int?
        t = Transaction()
        t.person=person
        form = NewTransactionForm(instance=t)
        return render(request, 'practice/newtransaction.html', {'form': form, 'person': person } )
    elif request.method == 'POST':
        form = NewTransactionForm(request.POST  )###########, instance=case)
        if form.is_valid():
            person = form.cleaned_data['person']
            dateposted = form.cleaned_data['dateposted']
            description = form.cleaned_data['description']
            transtype = form.cleaned_data['transtype']
            amount = form.cleaned_data['amount']
            transaction = Transaction(person=person,
                                      dateposted=dateposted,
                                      amount=amount,
                                      transtype=transtype,
                                      description=description)
            transaction.save()
            note = "edit transaction saved"
            return redirect('practice:rand')  # , {'note':note})#, {'person':person})
        else:
            note = "form not valid " + str(form.errors)
            return render(request, 'practice/newtransaction.html', {'form': form, 'note': note})


def edittransaction(request):
    note = 'edit transaction note'
    id = request.GET.get(ID, False) or request.POST.get(ID, 0)  # one or the other
    if not id:
        raise Exception("no id in request.method")
    transaction = Transaction.objects.get(pk=id)
    person = transaction.person
    if request.method == 'GET':
        form = TransactionForm(instance=transaction)
        return render(request, 'practice/edittransaction.html', dict(form=form, person=str(person))                      )
    else:  ########### request.method == 'POST':
        form =TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('practice:rand')
        else:
            note = 'some error'
            return render(request, 'practice/edittransaction.html', {'form': form, 'person': person, 'note':note } )
