from django import forms
from tasks.models import TaskEntry

class TaskEntryForm(forms.ModelForm):
    CATIGORY_CHOICES = [('HO', 'Home'),('SC','School'),('WO','Work'),('SI','Self Improvement'),('OT', 'Other')]
    description = forms.CharField(widget=forms.TextInput(attrs={'size':'80'}))
    catigory = forms.ChoiceField(choices=CATIGORY_CHOICES)

    class Meta():
        model = TaskEntry
        fields = ('description', 'catigory')
