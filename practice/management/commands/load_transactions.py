'''
Created on Jul 10, 2019

@author: fsells
'''

from django.core.management.base import BaseCommand, CommandError
from practice.models import Person, Case, Transaction, TransactionType

import csv, random

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass



    def handle(self, *args, **options):
        phrases = []
        INVOICE = TransactionType.objects.get(type="Invoice")
        for person in Person.objects.filter(lastname__istartswith='G'):
            cases = Case.objects.filter(person=person).order_by('begindate')
            for case in cases:
                t = Transaction(charge=case.trialfee, description='{} case {}'.format(case.description, case.casenum))
                t.save()
                print (person.lastname, case.description)
            # for i in range(3):
            #     phrase = random.choice(phrases)
            #     casenum = '{}{}'.format(random.randint(1111111, 9999999), random.randint(1111111, 9999999) )
            #     ############################################print (person.id, casenum, phrase)
            #     c = Case()
            #     c.casenum = casenum
            #     c.description = phrase
            #     c.person = person
            #     c.representationfee = 1000
            #     c.trialfee = 5000
            #     c.save()
            #
            
            
            
        