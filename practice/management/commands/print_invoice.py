'''
Created on Jul 10, 2019
CREATE INVOICE TEST
@author: fsells
'''
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from practice.models import Person, Case, Transaction, Template
from practice.docgen.statement_creator import StatementCreator
import datetime, os, io



class Command(BaseCommand):
    help = 'generate docx file for testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        transaction = Transaction.objects.get(pk=13)
        file = Template.objects.filter(description='invoice').order_by('-uploaded_at').first()
        print( file )
        #print (dir(file))

        formatter = StatementCreator(transaction)
        outpath = formatter.write_document(file.document.name)
        print('output written to ', outpath)
        return





            
            
        