from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
from django.db import models
from unittest.util import _MAX_LENGTH

DOCTYPE_CHOICES = [ ('invoice', 'Inovice'),
                    ('engagement', 'Engagement Ltr'),

                    ]



class DocxTemplate(models.Model):
    title = models.CharField(max_length=255, choices=DOCTYPE_CHOICES)
    location = models.FileField(upload_to='docx_templates/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'type={} uploaded on={}, file location={}'.format(self.title, self.uploaded_at, self.location)

    def get_path(self):
        return self.location.name

    class Meta:
        db_table = 'templates'
        managed = True


class TransactionType(models.Model):
    id = models.AutoField(primary_key=True, db_column='transactiontypeid')
    name = models.CharField(max_length=20)
    multiplier = models.IntegerField(default=0)  # +1= charge, 0=no impact, -1=payment
    #used with transaction amount to determine balance impact.

    def __unicode__(self):
        return 'transaction type={}, id={}, multiplier={}'.format(self.name, self.id, self.multiplier)

    def __str__(self):
        return '{} id={}, multiplier={}'.format(self.name, self.id, self.multiplier)

    class Meta:
        db_table = 'transactiontypes'
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
    salutation = models.ForeignKey(Salutation, db_column='salutationid', default='', on_delete=models.SET_NULL, null=True)
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=60)
    suffix = models.CharField(max_length=10, default='', help_text='used to differentiate people with same first and last name')
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

    def get_salutation(self):
        if self.salutation:
            text = self.salutation.description + ' '
        else:
            text = 'Mr. '
        text += self.lastname or 'LASTNAME NOT DEFINED'
        return 'Dear ' + text + ':'

    def get_mailing_address(self):
        items = [self.salutation, self.firstname, self.lastname, self.suffix]
        who = ' '.join(item for item in items if item) #eliminate empty fields
        csz = self.city  or 'NO CITY ENTERED'
        csz += ', '
        csz += self.state or 'ND'
        csz += '  '
        csz += self.zip or 'NOZIPCODE'
        lines = [who]
        lines.append(self.addr1)
        lines.append(self.addr2)
        lines.append(csz)
        block = '\n'.join( [line for line in lines if line]) #remove blank lines, i.e. addr2
        return block

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

    def __str__(self):
        return 'case id={}, client={}, case={}, begin={}, desc={}'.format(self.id, self.person.lastname, self.casenum, self.begindate, self.description)

    def is_valid(self):
        if self.description.lower().startswith('zz'): return False
        return True

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
    balancedue = models.DecimalField(max_digits=8, decimal_places=2, null=True )


    def __unicode__(self):
        return 'date posted={}, description={}, balance'.format( self.person.lastname, self.dateposted, self.description)

    def __str__(self):
        return 'date posted={}, description={}, type={} amount{}'.format(self.dateposted, self.description, self.transtype, self.amount)

    def get_balance_impact(self):
        return self.amount * self.transtype.multiplier

    class Meta:
        db_table = 'transactions'
        managed = True