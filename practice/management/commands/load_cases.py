'''
Created on Jul 10, 2019

@author: fsells
'''
from django.core.management.base import BaseCommand, CommandError
from practice.models import Person, Case

import csv, random

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        phrases = []
        with open('practice/management/commands/phrases.txt') as f:
            for line in f:
                phrase = line[:80]  #chop off end
                phrases.append(phrase)
        for person in Person.objects.all():
            for i in range(3):
                phrase = random.choice(phrases)
                casenum = '{}{}'.format(random.randint(1111111, 9999999), random.randint(1111111, 9999999) )
                ############################################print (person.id, casenum, phrase)
                c = Case()
                c.casenum = casenum
                c.description = phrase
                c.person = person
                c.representationfee = 1000
                c.trialfee = 5000
                c.save()
        
            
            
            
        