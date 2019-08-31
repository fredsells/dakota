from __future__ import absolute_import

import datetime, random
import datetime, os, io


from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
#################################from django.db.models import Count
from django.db.models.functions import Lower
from django.http import JsonResponse
#from rest_framework import viewsets
from django.contrib.auth.decorators import permission_required

from practice.docgen.generic_merge_manager import create_document
from practice.docgen.engagement_letter_parser import Parser

from practice.models import Person, Case

from .caseforms import NewCaseForm, CaseForm

def create_http_response( fullpath):
    filename = os.path.split(fullpath)[1]
    MSWORD_CONTENT_TYPE = 'application/vnd.ms-word'#.openxmlformats-officedocument.wordprocessingml.document'
    f = open(fullpath, 'rb')
    response = HttpResponse(f, content_type=MSWORD_CONTENT_TYPE)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


def print_transaction(case):
    stmt = Parser(case)
    path = create_document('engagement', case.person.lastname, None, rows=[], **stmt.get_fields())
    print(path)
    response = create_http_response(path)
    return response

ID = 'id'
def editcase(request):
    note = ''
    id = request.GET.get(ID, False) or request.POST.get(ID) #one or the other
    case = Case.objects.get(pk=id)
    title = str(case.person)
    if request.method == 'GET':
        form = CaseForm(instance=case)
        return render(request, 'practice/editcase.html', dict(form=form, title=title)
                      )
    else:  ##############must be request.method == 'POST':
        filled_form = CaseForm(request.POST, instance=case)
        if filled_form.is_valid():
            case = filled_form.save()
            if request.POST.get('print', True):
                return print_transaction(case)
            else:
                return redirect('practice:rand')  # , {'note':note})#, {'person':person})
        else:
            note = "form not valid " + str(filled_form.errors)
            print (filled_form.errors)
            return render(request, 'practice/editcase.html', dict(form=filled_form, note=note, title=title))



def newcase(request):
    note = ''
    if request.method == 'GET':
        clientid = request.GET['clientid']  # required; throw exception if missing
        person = Person.objects.get(pk=clientid)  # might have to change to int?
        initial_values = dict(person=person, auto_id=False)
        form = NewCaseForm(initial=initial_values)
        return render(request, 'practice/newcase.html', {'form':form, 'person' :str(person) } )
    elif request.method == 'POST':
        form = NewCaseForm(request.POST  )###########, instance=case)
        print ('===============post', request.POST )
        if form.is_valid():
            print('xxxxxxxxxxxxxxxxxxxxxxx', form.cleaned_data['begindate'])
            case = form.save()
            if request.POST.get('print', True):
                return print_transaction(case)
            else:
                return redirect('practice:rand'  )  # , {'note':note})#, {'person':person})
        else:
            person = request.POST.get('person')
            note = "form not valid " + str(form.errors)
            print (form.errors)
            return render(request, 'practice/newcase.html', {'form': form, 'note': note, 'title' :str(person)})
