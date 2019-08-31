
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from practice.models import Person, Case, Transaction
from mailmerge import MailMerge
import datetime
import os, io, ntpath

class Parser(object):

    def __init__(self, case):
        self.Case = case
        self.Person = case.person

    def get_rows(self):
        return []

    def get_fields(self, **kwargs):
        casenum = self.Case.casenum or "no case num yet>"
        description = self.Case.description

        parameters = dict(AddressBlock=self.Person.get_mailing_address(),
                               RepFee = '$%d' % self.Case.representationfee,
                               TrialFee = '$%d' % self.Case.trialfee,
                               CaseSummary = '%s:%s' % (casenum, description),
                               ClientName = '%s %s' % (self.Person.firstname, self.Person.lastname)
                               )
        parameters.update(kwargs)
        return parameters

