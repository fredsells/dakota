'''
Created on Jul 6, 2019

@author: fsells
'''
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from practice import views

app_name = 'practice'  #required to use practice as a qualifying namespace in template

# urlpatterns = [
#     path('', viewsobsolete.index, name='index'),    # ex: /practice/
#     path('<int:question_id>/', viewsobsolete.detail, name='detail'),     # ex: /practice/5/
#     path('specifics/<int:question_id>/', viewsobsolete.detail, name='detail'), #uses name to avoid code impact.
#     path('<int:question_id>/results/', viewsobsolete.results, name='results'),    # ex: /practice/5/results/
#     path('<int:question_id>/vote/', viewsobsolete.vote, name='vote'),     # ex: /practice/5/vote/
# 
# ]

#use generic viewsobsolete

urlpatterns = [
#    path('', views.IndexView.as_view(), name='index'),
#     path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#     path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
    path('home', views.home, name='home'),
    path('clients', views.ClientList.as_view(), name='clients'),
    path('invoices', views.InvoiceList.as_view(), name='invoices'),
    path('rand', views.RandD.as_view(), name='rand'),
    path('cases', views.get_cases, name='cases'),
 #   path('editclient/<int:pk>', views.editclient, name='editclient'),

    path('editclient', views.editclient, name='editclient'),
    path('newclient', views.newclient, name='newclient'),

    path('editcase', views.editcase, name='editcase'),
    path('newcase', views.newcase, name='newcase'),
    path('xxxx', views.InvoiceList.as_view(), name='xxxx'),

]