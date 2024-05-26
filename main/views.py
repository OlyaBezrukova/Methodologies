from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from model.models import Criterias, Options, Methodologies, Scores, CriteriasPriority
from django.contrib.auth.models import User

def index(request):
    
    return render(request, 'main/main.html')

def about(request):
    pass

def register_user(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        data = dict(request.POST.lists())

        if form.is_valid():
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            
            user = User.objects.get(username=data['username'][0])

            meths = Methodologies.objects.filter(access=1)
            
            for meth in meths:
                meth.access.add(user)
                meth.save()
            crits = Criterias.objects.filter(access=1)
            for crit in crits:
                crit.access.add(user)
                crit.save()

            return redirect("main:login")


    context = {'form': form}
    return render(request, 'main/reg.html', context)

def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main:main')
        else:
            messages.info(request, "Username OR password is inncorect")
        
    context = {
        'text': "Logout"
    }

    return render(request, 'main/login.html', context)

def logout_user(request):
    logout(request)
    return redirect("main:login")