from django.contrib import admin
from budget.models import BudgetEntry
from budget.models import BudgetCategory

# Register your models here.
admin.site.register(BudgetEntry)
admin.site.register(BudgetCategory)
