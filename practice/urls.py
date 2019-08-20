'''
Created on Jul 6, 2019

@author: fsells
'''
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from practice import views
from practice import edit_views

app_name = 'practice'  #required to use practice as a qualifying namespace in template



#use generic viewsobsolete

urlpatterns = [

    path('home', views.home, name='home'),
    path('clients', views.ClientList.as_view(), name='clients'),
    path('invoices', views.InvoiceList.as_view(), name='invoices'),
    path('rand', views.RandD.as_view(), name='rand'),
    path('cases', views.get_cases, name='cases'),

    path('getclients', views.get_clients, name='getclients'),
    path('editclient', edit_views.client.editclient, name='editclient'),
    path('newclient', edit_views.client.newclient, name='newclient'),

    path('editcase', edit_views.case.editcase, name='editcase'),
    path('newcase', edit_views.case.newcase, name='newcase'),

    path('transactions', views.get_transactions, name='transactions'),
    path('edittransaction', edit_views.edittransaction, name='edittransaction'),
    path('newtransaction', edit_views.newtransaction, name='newtransaction'),

    path('xxxx', views.InvoiceList.as_view(), name='xxxx'),

]

# urlpatterns = [
#     path('', viewsobsolete.index, name='index'),    # ex: /practice/
#     path('<int:question_id>/', viewsobsolete.detail, name='detail'),     # ex: /practice/5/
#     path('specifics/<int:question_id>/', viewsobsolete.detail, name='detail'), #uses name to avoid code impact.
#     path('<int:question_id>/results/', viewsobsolete.results, name='results'),    # ex: /practice/5/results/
#     path('<int:question_id>/vote/', viewsobsolete.vote, name='vote'),     # ex: /practice/5/vote/
#
# ]
#    path('', views.IndexView.as_view(), name='index'),
#     path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#     path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),