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

from .forms import NewPersonForm, PersonForm, NewCaseForm, CaseForm


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
        return render(request, 'practice/editclient.html', {'personform':form, 'note':note})

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
            return render(request, 'practice/editcase.html', {'form':filled_form, 'note':person.lastname})


    
####################### new client below ###################################################

def newclient(request):
    print ('\n\n\n =============================================newclient {} '.format(request.method) )
    note = ''
    if request.method == 'GET':
        person = Person()
        form = NewPersonForm(instance=person)
        return render(request, 'practice/newclient.html', {'form':form, 'note':note})
    elif request.method == 'POST':
        filled_form = NewPersonForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            return render(request, 'practice/rand.html')
        else:
            print (filled_form.errors)
            note = "some error"
            return render(request, 'practice/newclient.html', {'form':filled_form, 'note':note})






    
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
    
  

def editcase(request):
    note = ''
    if request.method == 'GET':
        caseid = request.GET['id']
        case = Case.objects.get(pk=caseid)
        form = CaseForm(instance=case)
        return render(request, 'practice/editcase.html', {'caseform': form,'client':case.person } )

    elif request.method == 'POST':
        print('----------post keys', request.POST.keys())
        caseid = request.POST['id']
        case = Case.objects.get(pk=caseid)
        filled_form = CaseForm(request.POST, instance=case)
        if filled_form.is_valid():
            filled_form.save()
            note = "edit case saved"
            return redirect('practice:rand')#, {'note':note})#, {'person':person})
        else:
            note = "form not valid " + str(filled_form.errors)
            print (filled_form.errors)
            return render(request, 'practice/editclient.html', {'form': filled_form, 'note': note})



def newcase(request):
    note = ''
    if request.method == 'GET':
        clientid = request.GET['clientid']  #required; throw exception if missing
        person = Person.objects.get(pk=clientid)  #might have to change to int?
        form = NewCaseForm(initial={'personid': person.id}, auto_id=False)
        return render(request, 'practice/newcase.html', {'form':form, 'person':person } )
    elif request.method == 'POST':
        form = NewCaseForm(request.POST)###########, instance=case)
        if form.is_valid():
            personid = form.cleaned_data['personid']
            person = Person.objects.get(pk=personid)
            casenum  = form.cleaned_data['casenum']
            description = form.cleaned_data['description']
            representationfee = form.cleaned_data['representationfee']
            trialfee = form.cleaned_data['trialfee']
            initialpayment = form.cleaned_data['initialpayment']
            begindate = form.cleaned_data['begindate']
            case = Case(person=person, casenum=casenum, description=description, representationfee=representationfee,
                        trialfee=trialfee, initialpayment=initialpayment, begindate=begindate)
            case.save()
            note = "edit case saved"
            return redirect('practice:rand')#, {'note':note})#, {'person':person})
        else:
            note = "form not valid " + str(form.errors)
            print (form.errors)
            return render(request, 'practice/newclient.html', {'form': form, 'note': note})
