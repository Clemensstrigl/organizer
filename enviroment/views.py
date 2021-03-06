from django.shortcuts import render
from django.shortcuts import redirect


from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from enviroment.forms import JoinForm, LoginForm
from tasks.models import TaskEntry
from budget.models import BudgetEntry

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def home(request):

    pieCompleted = 0
    pieUnfinished = 0

    userTasks = list(TaskEntry.objects.filter(user=request.user).values_list('complete',flat = True))
    for completed in userTasks:
        if(completed == True):
            pieCompleted +=1
        else:
            pieUnfinished += 1


    projectedList = list(BudgetEntry.objects.filter(user=request.user).values_list('projected',flat = True))
    actualList = list(BudgetEntry.objects.filter(user=request.user).values_list('actual',flat = True))
    userBudget = BudgetEntry.objects.filter(user=request.user)
    page_data = {'pieDataCompleted': pieCompleted, 'pieDataUnfinished':pieUnfinished, 'projectedList':projectedList, 'actualList': actualList}
    return render(request, 'enviroment/home.html', page_data)

def about(request):
    return render(request,'enviroment/about.html')

def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            user = join_form.save()
            user.set_password(user.password)
            user.save()
            login(request,user)
            return redirect("/")
        else:
            page_data = { "join_form": join_form }
            return render(request, 'enviroment/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = { "join_form": join_form }
        return render(request, 'enviroment/join.html', page_data)

def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect("/")
                else:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request, 'enviroment/login.html', {"login_form": LoginForm})
    else:
        return render(request, 'enviroment/login.html', {"login_form": LoginForm})

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect("/")
