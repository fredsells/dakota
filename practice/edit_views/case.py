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

ID = 'id'
def editcase(request):
    note = ''
    id = request.GET.get(ID, False) or request.POST.get(ID) #one or the other
    case = Case.objects.get(pk=id)
    title = str(case.person)
    if request.method == 'GET':
        form = CaseForm(instance=case)
        return render(request, 'practice/editcase.html', dict(form=form,
                                                              title=title)
                      )
    else:  ##############must be request.method == 'POST':
        filled_form = CaseForm(request.POST, instance=case)
        if filled_form.is_valid():
            filled_form.save()
            return redirect('practice:rand')  # , {'note':note})#, {'person':person})
        else:
            note = "form not valid " + str(filled_form.errors)
            print (filled_form.errors)
            return render(request, 'practice/editcase.html', dict(form=filled_form,
                                                                  note=note,
                                                                    title=title)
                          )



def newcase(request):
    note = ''
    if request.method == 'GET':
        clientid = request.GET['clientid']  # required; throw exception if missing
        person = Person.objects.get(pk=clientid)  # might have to change to int?
        initial_values = dict(person=person, auto_id=False)
        form = NewCaseForm(instance=person)
        return render(request, 'practice/newcase.html', {'form' :form, 'title' :str(person) } )
    elif request.method == 'POST':
        form = NewCaseForm(request.POST  )###########, instance=case)
        if form.is_valid():
            person = form.cleaned_data['person']
            #person = Person.objects.get(pk=personid)
            casenum  = form.cleaned_data['casenum']
            description = form.cleaned_data['description']
            representationfee = form.cleaned_data['representationfee']
            trialfee = form.cleaned_data['trialfee']
            initialpayment = form.cleaned_data['initialpayment']
            begindate = form.cleaned_data['begindate']
            case = Case(person=person, casenum=casenum, description=description, representationfee=representationfee,
                         trialfee=trialfee, initialpayment=initialpayment, begindate=begindate, enddate=begindate)
            case.save()
            note = "edit case saved"
            return redirect('practice:rand'  )  # , {'note':note})#, {'person':person})
        else:
            note = "form not valid " + str(form.errors)
            print (form.errors)
            return render(request, 'practice/newcase.html', {'form': form, 'note': note, 'title' :str(person)})
