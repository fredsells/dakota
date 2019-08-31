

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from practice.models import Person, Case, Transaction
from mailmerge import MailMerge
import datetime
import os, io, ntpath

class StatementCreator(object):

    def __init__(self, invoice):
        self.Invoice = invoice
        self.Person = person = invoice.person
        self.Cases = Case.objects.filter(person=person).order_by('begindate')
        self.Transactions = Transaction.objects.filter(person=person).order_by('dateposted')
        self.RepFees = self.Transactions.filter(transtype_id=1)#.values_list('amount', flat=True))
        self.TrialFees = self.Transactions.filter(transtype_id=2)#.values_list('amount', flat=True))
        self.Discounts = self.Transactions.filter(transtype_id=3)#.values_list('amount', flat=True))
        self.Payments = self.Transactions.filter(transtype_id=2)

        self.repfees = sum(self.RepFees.values_list('amount', flat=True))
        self.trialfees   = sum(self.TrialFees.values_list('amount', flat=True))
        self.discounts   = -sum(self.Discounts.values_list('amount', flat=True))
        self.TotalFees = self.repfees + self.trialfees + self.discounts
        self.BalanceDue = self.TotalFees - sum([x.amount for x in self.Payments])
        
    def get_mailing_address(self):
        return self.Person.get_mailing_address()

    def get_cases(self):
        return ', '.join([case.casenum for case in self.Cases])

    def get_fees(self):  #this is ugly because mailmerge cannot handle two tables.  fix with upgrade?
        lines = [('Flat fee for representation:', self.repfees),
                 ('Trial Fee:', self.trialfees),
                 ('Discounts:', self.discounts),
                 ('TOTAL FEES AND EXPENSES:',self.TotalFees),
                 ]
        lines = [(x[0], '$%.2f' % x[1]) for x in lines if x[1]]
        lines.insert(0, ('Description', 'Amount'))
        lines = ['%-40s %+10s' % x for x in lines]
        text = '\n'.join(lines)
        return text

    def get_rows(self):
        payments = list(self.Payments.values('id', 'dateposted', 'amount') )
        balance = self.TotalFees
        for p in payments:
            balance -= p['amount']
            p['invoice'] = '%s' % p['id']
            p['dateposted'] = str(p['dateposted'])
            p['payment'] = '$%.2f' % p['amount']
            p['balancedue'] = '$%.2f' % balance
            
        return payments
    
    

    def get_fields(self, **kwargs):
        self.parameters = dict(AddressBlock=self.Person.get_mailing_address(),
                                CaseNums = self.get_cases(),
                                Fees = self.get_fees(),
                                BalanceAsOfDate = str(datetime.date.today()),
                                BalanceDue = '$%.2f' % self.BalanceDue,
                                DueDate = str(self.Invoice.dateposted + datetime.timedelta(days=10)),
                                AmountDue = '$%.2f' % self.Invoice.amount,
                                ClientName = '%s %s' % (self.Person.firstname, self.Person.lastname)
                                )
        self.parameters.update(kwargs)
        return self.parameters

#     def get_output_path(self, path_to_template):
#         hhmm=datetime.datetime.now().strftime('%H%M')
#         outfile = self.Person.lastname + '_' + hhmm + '_' + 'statement.docx'
#         return os.path.join(settings.MEDIA_ROOT, 'tempfiles', outfile)
# 
#     def write_document(self, path_to_template):
#         self.build_parameters()
#         inpath = os.path.join(settings.MEDIA_ROOT, path_to_template )
#         print('inpath', inpath)
# 
#         outpath = self.get_output_path(path_to_template)
#         print('outpath', outpath)
#         tempdir = os.path.join(settings.MEDIA_ROOT, 'tempfiles')
#         # [os.unlink(file.path) for file in os.scandir(tempdir)]  #remove prior files
# 
#         print('outpath', outpath)
#         document = MailMerge(inpath)
#         print (self.parameters.keys())
#         temp = dict()
#         temp['AddressBlock'] = self.parameters['AddressBlock']
#         print (temp)
#         document.merge(temp)
#         for r in self.rows:
#             r['invoice'] = r['id']#print (r)
#         # document.merge_rows('invoice', self.rows)
#         document.write(outpath)
#         #document.close()
#         return outpath
