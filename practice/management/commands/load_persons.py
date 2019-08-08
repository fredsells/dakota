'''
Created on Jul 10, 2019

@author: fsells
'''
from django.core.management.base import BaseCommand, CommandError
from practice.models import Person
import random
import csv, os

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print(os.path.abspath( os.curdir) )
        with open('practice/management/commands/persons.csv') as f:
            reader = csv.reader(f)
            for r in reader:
                [id, fname, lname, email] = r
                p = Person()
                p.firstname=fname
                p.lastname = lname
                p.addr1 = "%s %s" % (random.randint(1111, 9999), random.choice( ['Main St', 'First Stree', 'Mayberry Ln']) )
                p.city = random.choice( ['Billings', "Sleepy Hollow", 'Evansville'])
                p.state = 'ND'
                p.zip ='12345'
                p.dob = None
                p.email = email
                p.save()
            
            
        