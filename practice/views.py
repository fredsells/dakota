'''
Created on Jul 7, 2019

@author: fsells
'''


import sys, os, datetime, random
from decimal import Decimal
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
#################################from django.db.models import Count
from django.db.models.functions import Lower
from django.db.models import Sum
from django.db.models import F
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required


import django.db.models.functions as x


#from rest_framework import viewsets
from django.contrib.auth.decorators import permission_required


from .models import Person, Case, Transaction, TransactionType


LETTER_DIR = settings.MEDIA_ROOT

def create_http_response(request, fullpath):
    MSWORD_CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    #response['Content-Disposition'] = 'attachment; filename=whatever.docx'
    f = open(fullpath, 'rb')
    response = HttpResponse(f, content_type=MSWORD_CONTENT_TYPE)
    return response



def test1(request, fullpath):
    return phase_one.create_merged_file(request, fullpath)

def home(request):
    return render(request, 'practice/home.html')


def get_cases(request):
    client_id = request.GET.get('id', None)
    person = Person.objects.get(pk=client_id)
    title = person.lastname + ', ' + person.firstname
    cases = Case.objects.filter(person=person).order_by('begindate')
    data = list(cases.values() )
    x = JsonResponse({'data': data, 'title':title, 'clientid':client_id})
    return x
    
def get_transactions(request):
    client_id = request.GET.get('id', None)
    person = Person.objects.get(pk=client_id)
    title = person.lastname + ', ' + person.firstname
    items = Transaction.objects.filter(person=person).select_related().order_by('dateposted')
    Balance = Decimal(0.00)
    values = list(items.values('person','transtype__name', 'id', 'dateposted', 'description',  'transtype__id') )
    for i,item in enumerate(items):
        x = dict()
        Balance += item.amount * item.transtype.multiplier
        charge = invoice = payment = ''
        if item.transtype.multiplier == 1: charge = item.amount
        elif item.transtype.multiplier == -1: payment = item.amount
        else: invoice = item.amount
        options = dict(balance=Balance, charge=charge, payment=payment, invoice = invoice)
        values[i].update(options)
    for v in values: print (v)
#    values = items.values()
    x = JsonResponse({'data': values, 'title':title, 'clientid':client_id})
    return x


def get_clients(request):
    print ('>>>>>>>>>>>>>>>>>>>>>>>>',request.user)
    items = Person.objects.all().select_related().order_by('lastname', 'firstname')
    values = items.values()
    data = list(values)
    return JsonResponse({'data': data, 'title':'', 'clientid':''})




    
class ClientList(generic.ListView):
    template_name = 'practice/clients.html'
    context_object_name = 'clients'

    def get_queryset(self):
        people = Person.objects.all().order_by(Lower('lastname'), Lower('firstname'))# not working .annotate(num_cases=Count(Case))
        for p in people: print(p.lastname)
 
class InvoiceList(generic.ListView):
    template_name = 'practice/invoices.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        items = Person.objects.all().order_by('lastname', 'firstname')# not working .annotate(num_cases=Count(Case))
        return items
    
 
class RandD(generic.ListView):
    template_name = 'practice/rand.html'
    context_object_name = 'items'

    def get_queryset(self):
        items = Person.objects.all().order_by(Lower('lastname'), Lower('firstname'))# not working .annotate(num_cases=Count(Case))
        ############################for x in items: print(x.lastname)
        return items
    
