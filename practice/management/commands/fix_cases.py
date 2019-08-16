'''
Created on Jul 10, 2019

@author: fsells
'''
from django.core.management.base import BaseCommand, CommandError
from practice.models import Person, Case

import csv, random, datetime


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        cases = Case.objects.all()
        for case in cases:
            d = random.randint(3, 400)
            case.begindate = case.begindate or (datetime.date.today() - datetime.timedelta(days=d))
            case.save()




