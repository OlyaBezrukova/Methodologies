from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .models import Criterias, Options, Methodologies, Scores, CriteriasPriority
from .topsis import Topsis
from .ahp import Ahp
import pandas as pd
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.db import migrations
from django.contrib.auth.models import User


RESULTS = []

def model_home(request):

    ahp = Ahp()
    global RESULTS
    data = []
    error = ''
    if request.user.is_authenticated:
        access=request.user
    else:
        access = User.objects.get(pk=1)
        
    for el in Criterias.objects.filter(access=access):

        element_name = el.name
        opts = [value.description for value in Options.objects.filter(criteria=el)]
        values = {element_name: opts}
        data.append(values)

    if request.method == 'POST':
        user_data = dict(list(request.POST.items())[1:])
        if (len(user_data) != len(data)):
            error = "Вам нужно оценить каждый критерий!"
        else:
            topsis = Topsis(access)
            topsis_results = topsis.get_results(response=user_data)
            RESULTS = pd.DataFrame(topsis_results)
            return redirect('model:results')
    return render(request, 'model/model_home.html', {'data': data, 'error': error})
    
def show_results(request):
    global RESULTS
    winner_methodology = list(RESULTS.index)[0]
    context = {
        'table': RESULTS[1:].to_html(), 
        'winner': winner_methodology.name, 
        'ideal': RESULTS.loc[winner_methodology, 'Distance to ideal'],
        'negative': RESULTS.loc[winner_methodology, 'Distance to negative'],
        }
    return render(request, 'model/results.html', context)
