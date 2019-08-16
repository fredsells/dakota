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


from .models import Person, Case


def home(request):
    return render(request, 'practice/home.html')


def get_cases(request):
    client_id = request.GET.get('id', None)
    person = Person.objects.get(pk=client_id)
    title = person.lastname + ', ' + person.firstname
    cases = Case.objects.filter(person=person).order_by('-begindate')
    data = list(cases.values() )
    ################################################################# for d in data: print(d)
    x = JsonResponse({'data': data, 'title':title, 'clientid':client_id})
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
    
