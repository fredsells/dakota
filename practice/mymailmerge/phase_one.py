from django.http import FileResponse
from mailmerge import MailMerge
import datetime, sys, os, io
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from tempfile import TemporaryFile

# def test1(request, fullpath, data=dict(lastname='Sells')):
#     response = HttpResponse('creating merge for {}'.format(fullpath))
#     return response


def test2(request, fullpath, data):
    response = FileResponse(open(fullpath, 'rb'))
    return response

def test3(request, fullpath, data):
    document = MailMerge(fullpath)
    document.merge(data)
    MSWORD_CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    http_word_response = HttpResponse(content_type=MSWORD_CONTENT_TYPE )
    http_word_response['Content-Disposition'] = 'attachment; filename=whatever.docx'
    document.write(http_word_response)
    document.close()
    http_word_response.close()
    return http_word_response
    # print(response)
    # return response


def create_merged_file(request, fullpath, data=dict(lastname='Sells')):
    data = dict(AddressBlock='123 Main Street', fredtest='Yo Fred', salutation='Doctor')
    return test3(request, fullpath, data)
