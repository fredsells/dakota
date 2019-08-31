
import datetime, random
import datetime, os, io


from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.urls import reverse
from django.views import generic
#################################from django.db.models import Count
from django.db.models.functions import Lower
from django.http import JsonResponse
#from rest_framework import viewsets
from django.contrib.auth.decorators import permission_required


from practice.models import Person, Case, Transaction, TransactionType, DocxTemplate
from practice.docgen.statement_creator import StatementCreator
from practice.docgen.generic_merge_manager import create_document

from .transactionforms import NewTransactionForm, TransactionForm

ID='id'


def create_http_response( fullpath):
    filename = os.path.split(fullpath)[1]
    MSWORD_CONTENT_TYPE = 'application/vnd.ms-word'#.openxmlformats-officedocument.wordprocessingml.document'
    f = open(fullpath, 'rb')
    response = HttpResponse(f, content_type=MSWORD_CONTENT_TYPE)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


def print_transaction(transaction):
    stmt = StatementCreator(transaction)
    path = create_document('invoice', transaction.person.lastname, 'invoice', rows=stmt.get_rows(), **stmt.get_fields())
    print(path)
    response = create_http_response(path)
    return response

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
            if request.POST.get('print', True) and transaction.transtype.name == 'Invoice':
                 return print_transaction(transaction)
            else:
                return redirect('practice:rand')  # , {'note':note})#, {'person':person})
        else:
            note = "form not valid " + str(form.errors)
            return render(request, 'practice/newtransaction.html', {'form': form, 'note': note})


def edittransaction(request):
    print ('edit transaction', request.method)
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
            transaction = form.save()
            print(transaction.id)
            if request.POST.get('print', True) and transaction.transtype.name == 'Invoice':
                 return print_transaction(transaction)
            else:
                return redirect('practice:rand')
        else:
            note = 'some error'
            return render(request, 'practice/edittransaction.html', {'form': form, 'person': person, 'note':note } )
