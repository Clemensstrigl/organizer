from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from tasks.models import TaskEntry
from tasks.forms import TaskEntryForm
from django.contrib.auth.models import User
from django.shortcuts import render

@login_required(login_url='/login/')
def tasks(request):
	if (request.method == "GET" and "delete" in request.GET):
		id = request.GET["delete"]
		TaskEntry.objects.filter(id=id).delete()
		return redirect("/task/")
	else:
        CATIGORY_CHOICES = {
        'HO':'Home',
        'SC':'School',
        'WO':'Work',
        'SI':'Self Improvement',
        'OT':'Other'
        }

        table_data = TaskEntry.objects.filter(user=request.user)
        for catigory in table_data:
            table_data[catigory] = CATIGORY_CHOICES[catigory]

		context = {
            "table_data": table_data
		}
		return render(request, 'tasks/tasks.html', context)

@login_required(login_url='/login/')
def add(request):
	if (request.method == "POST"):
		if ("add" in request.POST):
			add_form = TaskEntryForm(request.POST)
			if (add_form.is_valid()):
				description = add_form.cleaned_data["description"]
				catigory = add_form.cleaned_data["catigory"]
				user = User.objects.get(id=request.user.id)
				TaskEntry(user=user, description=description, catigory=catigory, complete=False).save()
				return redirect("/tasks/")
			else:
				context = {
                    "form_data": add_form
				}
				return render(request, 'tasks/add.html', context)
		else:
			# Cancel
			return redirect("/tasks/")
	else:
		context = {
            "form_data": TaskEntryForm()
		}
		return render(request, 'tasks/add.html', context)

@login_required(login_url='/login/')
def edit(request, id):
	if (request.method == "GET"):
		# Load Journal Entry Form with current model data.
		taskEntry = TaskEntry.objects.get(id=id)
		form = JournalEntryForm(instance=taskEntry)
		context = {"form_data": form}
		return render(request, 'tasks/edit.html', context)
	elif (request.method == "POST"):
		# Process form submission
		if ("edit" in request.POST):
			form = TaskEntryForm(request.POST)
			if (form.is_valid()):
				taskEntry = form.save(commit=False)
				tasklEntry.user = request.user
				taskEntry.id = id
				taskEntry.save()
				return redirect("/task/")
			else:
				context = {
                    "form_data": form
				}
				return render(request, 'task/add.html', context)
		else:
			#Cancel
			return redirect("/journal/")
