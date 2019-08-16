

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


from practice.models import Person, Case

from .clientforms import NewPersonForm, PersonForm

def editclient(request):
    print ('\n\n\n =============================================editclient {} '.format(request.method) )
    note = ''

    if request.method == 'GET':
        pk = request.GET.get('id', None)
        if pk:
            xid = int(pk)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>', xid, type(Person.objects))
            person = get_object_or_404(Person, pk=xid)
            print('person===========', person)
            form = PersonForm(instance=person)
        else:
            form = PersonForm()
        return render(request, 'practice/editclient.html', {'personform' :form, 'note' :note})

    elif request.method == 'POST':
        print( '==========================\npost parms', request.POST.items())
        id = request.POST.get('id', None)
        if not id:
            person = Person()
        else:
            person = Person.objects.get(pk=id)
        filled_form = PersonForm(request.POST, instance=person)
        if filled_form.is_valid():
            filled_form.save()
            return render(request, 'practice/rand.html')
        else:
            return render(request, 'practice/editcase.html', {'form' :filled_form, 'note' :person.lastname})



####################### new client below ###################################################

def newclient(request):
    print ('\n\n\n =============================================newclient {} '.format(request.method) )
    note = ''
    if request.method == 'GET':
        person = Person()
        form = NewPersonForm(instance=person)
        return render(request, 'practice/newclient.html', {'form' :form, 'note' :note})
    elif request.method == 'POST':
        filled_form = NewPersonForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            return render(request, 'practice/rand.html')
        else:
            print (filled_form.errors)
            note = "some error"
            return render(request, 'practice/newclient.html', {'form' :filled_form, 'note' :note})



