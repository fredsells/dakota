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

hhmm = datetime.datetime.now().strftime('%M%S')  
outfile = 'fredstest-'+ hhmm +'.docx'
INPUTPATH = os.path.join(settings.MEDIA_ROOT, 'documents', 'invoice03.docx')

OUTPUTPATH = os.path.join(settings.MEDIA_ROOT, 'tempfiles', outfile)
print(INPUTPATH)
print(OUTPUTPATH)
print('------------------------------------------------------------')


    
def get_fields():
    fees = [ ('Representation Fee', '$99.99'),
             ( 'Trial Fee', '$44.44'),
             ( 'Total','$77.77'),
             ]
    fees = '\n'.join(['%-40s  %8s' % fee for fee in fees])
    address = 'John Doe\n11 Main Street\nApt 102\nAnytown USA ND 32751'
    casenums = '111111111111, 222222222222, 3333333333333, 44444444444,55555555555'
    data = dict(AddressBlock=address, 
                Fees = fees, 
                CaseNums=casenums,
                AmountDue = '44.44',
                DueDate = '9/15/2019',
                BalanceAsOfDate='9/1/2019',
                ClientName = 'John Doe',
                BalanceDue='$1111.22')
    return data

def get_rows():
    return [dict(invoice='111', dateposted='3/4/2019', amount='$50.00', payment='$45.99', balancedue='$99,999.88'),
            dict(invoice='222', dateposted='3/4/2019', amount='$50.00', payment='$45.99', balancedue='$99,999.88'),
            dict(invoice='333', dateposted='3/4/2019', amount='$50.00', payment='$45.99', balancedue='$99,999.88'),
            ]    

class Command(BaseCommand):
    help = 'generate docx file for testing'

    def add_arguments(self, parser):
        pass
    
    def brute_force(self):
        document = mailmerge.MailMerge(INPUTPATH)
        document.merge( **get_fields() )
        document.merge_rows('invoice', get_rows())
        document.write( OUTPUTPATH)
        document.close()
        
    def get_temporary_path(self, person, doctype, root=settings.MEDIA_ROOT):
        hhmm = datetime.datetime.now().strftime('%H%M%S')  
        outfile = '%s-%s-%s.docx' % (person.lastname, doctype, hhmm )
        return os.path.join(root,  outfile) 
    
    def get_msword_template_path(self, doctype, root=settings.MEDIA_ROOT):
        shortpath = DocxTemplate.objects.filter(title=doctype).order_by('uploaded_at').first().get_path() #get most recent
        fullpath = os.path.join(root, shortpath)
        return fullpath
              
    def eazy_merge(self, document, rowname, rows=[], **kwargs):
        document.merge( **kwargs )
        if rows:
            document.merge_rows(rowname, rows)
        
        
    def sophisticated(self, transaction, xxtemplate, outfile):
        msword_template = self.get_msword_template_path('invoice')
        document = mailmerge.MailMerge(msword_template)
        stmt = StatementCreator(transaction)
        self.eazy_merge(document, 'invoice', stmt.get_payments(), **stmt.get_fields())
        temproot = os.path.join(settings.MEDIA_ROOT, 'tempfiles')
        outfile = self.get_temporary_path(transaction.person, 'statement', root=temproot)
        print('outfile', outfile)
        document.write(outfile)
        document.close()
        time.sleep(1)
       
    def planB(self, transaction):
        from practice.docgen.generic_merge_manager import create_document
        stmt = StatementCreator(transaction)
        path = create_document('invoice',  transaction.person.lastname, 'invoice', rows=stmt.get_rows(),  **stmt.get_fields())
        print (path)

        
    def handle(self, *args, **options):
        transaction = Transaction.objects.get(pk=13)
        self.planB(transaction)
#        self.brute_force()
#         msword_template = ''#os.path.join(settings.MEDIA_ROOT, file.location.name)
#         outfile = OUTPUTPATH
#         self.sophisticated(transaction, msword_template, outfile)
#        

        
#         file = Template.objects.filter(description='invoice').order_by('-uploaded_at').first()
#         print(file)
#         # print (dir(file))
# 
#         formatter = StatementCreator(transaction)
#         outpath = formatter.write_document(file.document.name)
#         print('output written to ', outpath)
#         return







