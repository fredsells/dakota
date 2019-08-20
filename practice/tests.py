from django.test import TestCase

# Create your tests here.


from models import *

class TransactionTestClass(TestCase):

    def test1(self):
        p = Person.objects.get(pk=51)
        trans = Transaction.objects.select_related().filter(person=p)


        self.assertFalse(False)


