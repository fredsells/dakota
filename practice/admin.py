from django.contrib import admin
from practice import models

# Register your models here.
admin.site.register(models.Salutation)
admin.site.register(models.TransactionType)
admin.site.register(models.DocxTemplate)
