from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from budget.models import BudgetEntry
from budget.forms import BudgetEntryForm
from budget.models import BudgetCategory
from django.contrib.auth.models import User
from django.shortcuts import render

@login_required(login_url='/login/')
def budget(request):

	if (request.method == "GET" and "delete" in request.GET):
		id = request.GET["delete"]
		BudgetEntry.objects.filter(id=id).delete()
		return redirect("/budget/")
	else:
		table_data = BudgetEntry.objects.filter(user=request.user)

		projectedTotal = 0
		actualTotal = 0
		for budgetE in table_data:
			projectedTotal += budgetE.projected
			actualTotal += budgetE.actual

		total = projectedTotal-actualTotal
		total = round(total, 2)
		context = {
            "table_data": table_data,
			"totalSpendDifference": total
		}
		return render(request, 'budget/budget.html', context)






def load_categories(request):
    categories = BudgetCategory.values('category').order_by('category')
    return render(request, 'tasks/category_dropdown_options.html', {'categories': categories})


@login_required(login_url='/login/')
def add(request):

	if(BudgetCategory.objects.count() == 0):
		BudgetCategory.objects.create(category="Food")
		BudgetCategory.objects.create(category="Clothing")
		BudgetCategory.objects.create(category="Hausing")
		BudgetCategory.objects.create(category="Education")
		BudgetCategory.objects.create(category="Entertainment")
		BudgetCategory.objects.create(category="Others")



	if (request.method == "POST"):
		if ("add" in request.POST):
			add_form = BudgetEntryForm(request.POST)
			if (add_form.is_valid()):
				description = add_form.cleaned_data["description"]
				category = BudgetCategory.objects.get(category=add_form.cleaned_data["category"])
				user = User.objects.get(id=request.user.id)
				projected = add_form.cleaned_data["projected"]
				actual = add_form.cleaned_data["actual"]

				BudgetEntry(user=user, description=description, category=category, projected=projected, actual=actual).save()
				return redirect("/budget/")
			else:
				context = {
                    "form_data": add_form
				}
				return render(request, 'budget/add.html', context)
		else:
			# Cancel
			return redirect("/budget/")
	else:
		context = {
            "form_data": BudgetEntryForm()
		}
		return render(request, 'budget/add.html', context)

@login_required(login_url='/login/')
def edit(request, id):
	if (request.method == "GET"):
		# Load Journal Entry Form with current model data.
		budgetEntry = BudgetEntry.objects.get(id=id)
		form = BudgetEntryForm(instance=budgetEntry)
		context = {"form_data": form}
		return render(request, 'budget/edit.html', context)
	elif (request.method == "POST"):
		# Process form submission
		if ("edit" in request.POST):
			form = BudgetEntryForm(request.POST)
			if (form.is_valid()):
				budgetEntry = form.save(commit=False)
				budgetEntry.user = request.user
				budgetEntry.id = id
				budgetEntry.save()
				return redirect("/budget/")
			else:
				context = {
                    "form_data": form
				}
				return render(request, 'budget/add.html', context)
		else:
			#Cancel
			return redirect("/budget/")
