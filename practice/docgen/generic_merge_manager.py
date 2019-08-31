'''
Created on Jul 10, 2019
CREATE INVOICE TEST
@author: fsells
'''


from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from practice.models import Person, Case, Transaction, DocxTemplate
from practice.docgen.statement_creator import StatementCreator
import datetime, os, io, time
import mailmerge

def get_temporary_path(lastname, doctype, root=settings.MEDIA_ROOT):
    hhmm = datetime.datetime.now().strftime('%H%M%S')
    outfile = '%s-%s-%s.docx' % (lastname, doctype, hhmm )
    return os.path.join(root,  outfile)

def get_msword_template_path( doctype, root=settings.MEDIA_ROOT):
    shortpath = DocxTemplate.objects.filter(title=doctype).order_by('uploaded_at').first().get_path()  # get most recent
    fullpath = os.path.join(root, shortpath)
    return fullpath

def eazy_merge(document, rowname, rows=[], **kwargs):
    document.merge( **kwargs )
    if rows:
        document.merge_rows(rowname, rows)


def create_document(doctype, lastname, rowname, rows=[], **kwargs):
    msword_template = get_msword_template_path(doctype)
    document = mailmerge.MailMerge(msword_template)
    eazy_merge(document, rowname, rows, **kwargs)
    temproot = os.path.join(settings.MEDIA_ROOT, 'tempfiles')
    outfile = get_temporary_path(lastname, doctype, root=temproot)
    print('outfile', outfile)
    document.write(outfile)
    document.close()
    time.sleep(1)
    return(outfile)




def manager(doctype, statement,  **options):
    msword_template = self.get_msword_template_path('invoice')
    outputpath = _create_document(statement, )
    transaction = Transaction.objects.get(pk=13)
    msword_template = '  '  # os.path.join(settings.MEDIA_ROOT, file.location.name)
    outfile = OUTPUTPATH
    self.sophisticated(transaction, msword_template, outfile)

