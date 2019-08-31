
import sys, datetime, io, os

from django.test import TestCase
from django.conf import settings
print(sys.path)
print(dir(settings))

from practice.models import Person


# Create your tests here.


#note this uses a test database, so the real data is not there :(

class TransactionTestClass(TestCase):

    def setUp(self) -> None:
        pass

    def oootest_address_block(self):
        person = Person.objects.get(id=51)
        text = person.get_mailing_address()
        print(text)
        self.assertFalse(False)


