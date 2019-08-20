'''
Created on Jul 7, 2019

@author: fsells
'''
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


from .models import Person, Case, Transaction, TransactionType


def home(request):
    return render(request, 'practice/home.html')


def get_cases(request):
    client_id = request.GET.get('id', None)
    person = Person.objects.get(pk=client_id)
    title = person.lastname + ', ' + person.firstname
    cases = Case.objects.filter(person=person).order_by('-begindate')
    data = list(cases.values() )
    x = JsonResponse({'data': data, 'title':title, 'clientid':client_id})
    return x
    
def get_transactions(request):
    client_id = request.GET.get('id', None)
    person = Person.objects.get(pk=client_id)
    title = person.lastname + ', ' + person.firstname
    items = Transaction.objects.filter(person=person).select_related().order_by('-dateposted')
    values = items.values('person','transtype__name', 'id', 'dateposted', 'description', 'amount', 'transtype__id')
#    values = items.values()
    data = list(values)
    x = JsonResponse({'data': data, 'title':title, 'clientid':client_id})
    return x

def get_clients(request):
    items = Person.objects.all().order_by('lastname', 'firstname')
    values = items.values()
    data = list(values)
    x = JsonResponse({'data': data, 'title':'', 'clientid':''})
    return x




    
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
    
