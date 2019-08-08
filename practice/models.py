from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
from django.db import models
from unittest.util import _MAX_LENGTH

# Create your models here.
class Person(models.Model):
    id = models.IntegerField(primary_key=True, db_column='personid')
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=60)
    ssn = models.CharField(max_length=12, null=True, blank=True, default='')
    dob = models.DateField(null=True)
    addr1 = models.CharField(max_length=40, null=True, blank=True, default='')
    addr2 = models.CharField(max_length=40, null=True, blank=True, default='')
    city = models.CharField(max_length=40, null=True, blank=True, default='')
    state = models.CharField(max_length=2, null=True, blank=True, default='')
    zip = models.CharField(max_length=10, null=True, blank=True, default='')
    email = models.EmailField(max_length=50, null=True, blank=True, default='')

    def __unicode__(self):
        return 'name={}, id={}'.format((self.lastname, self.personid))

    class Meta:
        db_table = 'persons'
        managed = True


class Case(models.Model):
    id = models.IntegerField(primary_key=True, db_column='caseid')
    person = models.ForeignKey(Person, db_column='personid', null=True, on_delete=models.SET_NULL)
    casenum = models.CharField(max_length=14, null=True, default='')
    description = models.TextField(max_length=60, null=True, default='', blank=True)
    representationfee = models.DecimalField(max_digits=8, decimal_places=2, null=True )
    trialfee = models.DecimalField(max_digits=8, decimal_places=2, null=True )
    initialpayment = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    begindate = models.DateField(null=True)
    enddate = models.DateField(null=True)

    def __unicode__(self):
        return 'case id={}, client={}'.format( self.id, self.person.lastname)

    class Meta:
        db_table = 'cases'
        managed = True



