from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from tasks.models import TaskEntry
from tasks.forms import TaskEntryForm
from tasks.models import TaskCategory
from django.contrib.auth.models import User
from enviroment.models import UserProfile
from django.shortcuts import render

def showAllTasks(UserProfile, TaskEntry, request):
	UserProfile.objects.filter(user=request.user).delete()
	UserProfile(user=request.user, tasks_view_hide_completed=False).save()
	table_data = TaskEntry.objects.filter(user=request.user)
	context = {
		"table_data": table_data,
		"task_view_status": False,
	}
	return render(request, 'tasks/tasks.html', context)

def hideAllCompleted(UserProfile, TaskEntry, request):
	UserProfile.objects.filter(user=request.user).delete()
	UserProfile(user=request.user, tasks_view_hide_completed=True).save()
	table_data = TaskEntry.objects.filter(user=request.user, complete=False)
	context = {
		"table_data": table_data,
		"task_view_status": True,
	}
	return render(request, 'tasks/tasks.html', context)



@login_required(login_url='/login/')
def tasks(request):
	task_view_status = UserProfile.objects.filter(user=request.user).values('tasks_view_hide_completed')[0]['tasks_view_hide_completed']
	if (request.method == "GET" and "delete" in request.GET):
		id = request.GET["delete"]
		TaskEntry.objects.filter(id=id).delete()
		return redirect("/tasks/")
	elif (request.method == "POST" and "tasks_view_hide_completed" in request.POST):
		if(task_view_status == True):
			return showAllTasks(UserProfile, TaskEntry, request)
		else:
			return hideAllCompleted(UserProfile, TaskEntry, request)
	else:
		if(task_view_status == False):
			return showAllTasks(UserProfile, TaskEntry, request)
		else:
			return hideAllCompleted(UserProfile, TaskEntry, request)



def taskCompleted(request):
	task_id=request.GET.get('task_id')
	print(task_id)
	currentTask = TaskEntry.objects.get(id=task_id)
	taskState = False
	if(currentTask.complete):
		currentTask.complete = False
	else:
		currentTask.complete = True
		taskState = True

	currentTask.save()
	return render(request, 'tasks/completeTaskChange.html', {"taskState" : taskState})



def load_categories(request):
    categories = TaskCategory.values('category').order_by('category')
    return render(request, 'tasks/category_dropdown_options.html', {'categories': categories})


@login_required(login_url='/login/')
def add(request):

	if(TaskCategory.objects.count() == 0):
		TaskCategory.objects.create(category="Home")
		TaskCategory.objects.create(category="School")
		TaskCategory.objects.create(category="Work")
		TaskCategory.objects.create(category="Self Improvement")
		TaskCategory.objects.create(category="Other")

	print(TaskCategory.objects.count())




	if (request.method == "POST"):
		if ("add" in request.POST):
			add_form = TaskEntryForm(request.POST)
			if (add_form.is_valid()):
				description = add_form.cleaned_data["description"]
				category = TaskCategory.objects.get(category=add_form.cleaned_data["category"])
				user = User.objects.get(id=request.user.id)

				TaskEntry(user=user, description=description, category=category, complete=False).save()
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
		form = TaskEntryForm(instance=taskEntry)
		context = {"form_data": form}
		return render(request, 'tasks/edit.html', context)
	elif (request.method == "POST"):
		# Process form submission
		if ("edit" in request.POST):
			form = TaskEntryForm(request.POST)
			if (form.is_valid()):
				taskEntry = form.save(commit=False)
				taskEntry.user = request.user
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
			return redirect("/tasks/")
