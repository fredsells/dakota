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

from .caseforms import NewCaseForm, CaseForm


def editcase(request):
    note = ''
    if request.method == 'GET':
        caseid = request.GET['id']
        case = Case.objects.get(pk=caseid)
        form = CaseForm(instance=case)
        return render(request, 'practice/editcase.html', {'caseform': form ,'client' :case.person } )

    elif request.method == 'POST':
        print('----------post keys', request.POST.keys())
        caseid = request.POST['id']
        case = Case.objects.get(pk=caseid)
        filled_form = CaseForm(request.POST, instance=case)
        if filled_form.is_valid():
            filled_form.save()
            note = "edit case saved"
            return redirect('practice:rand'  )  # , {'note':note})#, {'person':person})
        else:
            note = "form not valid " + str(filled_form.errors)
            print (filled_form.errors)
            return render(request, 'practice/editclient.html', {'form': filled_form, 'note': note})



def newcase(request):
    note = ''
    if request.method == 'GET':
        clientid = request.GET['clientid']  # required; throw exception if missing
        person = Person.objects.get(pk=clientid)  # might have to change to int?
        form = NewCaseForm(initial={'personid': person.id}, auto_id=False)
        return render(request, 'practice/newcase.html', {'form' :form, 'person' :person } )
    elif request.method == 'POST':
        form = NewCaseForm(request.POST  )###########, instance=case)
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
            return redirect('practice:rand'  )  # , {'note':note})#, {'person':person})
        else:
            note = "form not valid " + str(form.errors)
            print (form.errors)
            return render(request, 'practice/newclient.html', {'form': form, 'note': note})
