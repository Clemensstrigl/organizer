from django import forms
from budget.models import BudgetEntry
from budget.models import BudgetCategory

class BudgetEntryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size':'80'}))
    projected = forms.FloatField()
    actual = forms.FloatField()
    #CATEGORY_CHOICES = ['Home','School', 'Work','Self Improvement', 'Other']
#    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta():
        model = BudgetEntry
        fields = ('description', 'category', 'projected','actual')

    #def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        #self.fields['category'].queryset = TaskCategory.objects.none()
