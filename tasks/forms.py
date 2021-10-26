from django import forms
from tasks.models import TaskEntry
from tasks.models import TaskCategory

class TaskEntryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size':'80'}))
    #CATEGORY_CHOICES = ['Home','School', 'Work','Self Improvement', 'Other']
#    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta():
        model = TaskEntry
        fields = ('description', 'category')

    #def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        #self.fields['category'].queryset = TaskCategory.objects.none()
