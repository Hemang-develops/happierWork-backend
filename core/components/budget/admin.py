from django.contrib import admin
from .models import BudgetData

@admin.register(BudgetData)
class BudgetDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'designation', 'department', 'budget', 'location', 'lastUpdated0', 'lastUpdated1')
