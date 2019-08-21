from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
from django.db import models
from unittest.util import _MAX_LENGTH

class TransactionType(models.Model):
    id = models.AutoField(primary_key=True, db_column='transactiontypeid')
    name = models.CharField(max_length=20)
    multiplier = models.IntegerField(default=0)  # +1= charge, 0=no impact, -1=payment
    #used with transaction amount to determine balance impact.

    def __unicode__(self):
        return 'transaction type={}, id={}, multiplier={}'.format(self.name, self.id, self.multiplier)

    def __str__(self):
        return '{}, multiplier={}'.format(self.name, self.multiplier)

    class Meta:
        db_table = 'transactiontypes'
        managed = True

class PaymentType(models.Model):
    id = models.IntegerField(primary_key=True, db_column='paymenttypeid')
    type = models.CharField(max_length=10)

    def __unicode__(self):
        return 'type={}, id={}'.format((self.type, self.id))

    class Meta:
        db_table = 'paymenttypes'
        managed = True


class Salutation(models.Model):
    id = models.AutoField(primary_key=True, db_column='salutationid')
    salutation = models.CharField(max_length=10)

    def __unicode__(self):
        return 'salutation={}, id={}'.format((self.salutation, self.id))

    def __str__(self):
        return 'salutation: ' + self.salutation

    class Meta:
        db_table = 'salutations'
        managed = True


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
        return 'name={}, id={}'.format((self.lastname, self.id))

    def __str__(self):
        return '{},{}  id={}'.format(self.lastname, self.firstname, self.id)

    class Meta:
        db_table = 'persons'
        managed = True


class Case(models.Model):
    id = models.IntegerField(primary_key=True, db_column='caseid')
    person = models.ForeignKey(Person, db_column='personid', null=True, on_delete=models.SET_NULL)
    casenum = models.CharField(max_length=14, null=True, default='', blank=True)
    description = models.CharField(max_length=80, null=True, default='', blank=True)
    representationfee = models.DecimalField(max_digits=8, decimal_places=2, null=True )
    trialfee = models.DecimalField(max_digits=8, decimal_places=2, null=True )
    initialpayment = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    begindate = models.DateField(null=True, default='', blank=True)
    enddate = models.DateField(null=True, default=None)

    def __unicode__(self):
        return 'case id={}, client={}'.format( self.id, self.person.lastname)

    class Meta:
        db_table = 'cases'
        managed = True


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True, db_column='transactionid')
    person = models.ForeignKey(Person, db_column='personid', null=True, on_delete=models.SET_NULL)
    dateposted = models.DateField(default=datetime.date.today)
    transtype = models.ForeignKey(TransactionType, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=60, null=True, default='', blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True )


    def __unicode__(self):

        return 'date posted={}, description={}, balance'.format( self.person.lastname, self.dateposted, self.description)
    def __str__(self):
        return 'date posted={}, description={}, balance{}'.format( self.person.lastname, self.dateposted, self.description)

    class Meta:
        db_table = 'transactions'
        managed = True