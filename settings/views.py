from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from model.models import Criterias, Options, Methodologies, Scores, CriteriasPriority
import pandas as pd
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from .forms import MethodologyForm, CriteriaForm, OptionsForm, ScoresForm, PrioritiesForm
from django.contrib.auth.models import User

@login_required(login_url='/login')
def settings(request):
    meths = [value for value in list(Methodologies.objects.filter(access=request.user))]
    criterias = [value for value in list(Criterias.objects.filter(access=request.user))]
    context = {
        'meths': meths,
        'criterias': criterias,
    }
    return render(request, 'settings/settings_main.html', context)


def add_meth(request):
    error = ''
    if request.method =='POST':
        data = dict(request.POST.lists())
        access = []
        access.append(request.user)
        meth_data = {
            'name': data['name'][0],
            'access': access
        }
        form = MethodologyForm(meth_data)  
        if form.is_valid():
            meth = form.save()
            return redirect(reverse('settings:add_scores_meth', kwargs={'pk': meth.pk}))
        else:
            error = "Ошибка"

    form = MethodologyForm()
    context = {
        'form': form,
        'error': error,
        'title': "Добавить методологию",
        'btn': "Сохранить"
    }
    return render(request, 'settings/add_meth.html', context)

class MethUpdate(UpdateView):
    model = Methodologies
    template_name = 'settings/add_meth.html'
    form_class = MethodologyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование методологии" 
        context['btn'] = "Сохранить"
        return context
    
    def post(self, request, **kwargs):
        data = dict(request.POST.lists())

        users =  list(self.get_object().access.all())
        access = []
        if len(users) > 1:
            access.append(request.user)
        else:
            access = users

        meth_data = {
            'name': data['name'][0],
            'access': access
        }

        if len(users) > 1:
            meth_form = MethodologyForm(meth_data)
            self.get_object().access.remove(request.user)
        else:
            meth_form = MethodologyForm(meth_data, instance=self.get_object())

        if meth_form.is_valid():
            meth = meth_form.save()
            if len(users) > 1:
                scores = [score for score in list(Scores.objects.filter(methodology=self.get_object()))]
                for score in scores:
                    data = {
                        'methodology': meth,
                        'option': score.option,
                        'score': score.score
                    }

                    form = ScoresForm(data)

                    if form.is_valid():
                        form.save()
        else:
            error = "Ошибка"

        return redirect(reverse('settings:update_scores_meth', kwargs={'pk': meth.pk}))


class MethDelete(DeleteView):
    model = Methodologies
    success_url = '/settings/'
    template_name = 'settings/add_meth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meth_pk = self.get_object().pk
        meth_name = self.get_object().name
        data = {
            'name': meth_name
        }
        form = MethodologyForm(data)
        context['form'] = form
        context['title'] = "Удалить?"
        context['btn'] = "Удалить"
        return context
    
    def post(self, request, **kwargs):
        users =  list(self.get_object().access.all())

        if len(users) > 1:
            self.get_object().access.remove(request.user)
        else:
            self.get_object().delete()

        return redirect("settings:settings")


def return_base(request):
    meths = Methodologies.objects.filter(access=request.user)
    for meth in meths:
        if len(list(meth.access.all())) == 1:
            meth.delete()
    crits = Criterias.objects.filter(access=request.user)
    for crit in crits:
        if len(list(crit.access.all())) == 1:
            crit.delete()

    meths = Methodologies.objects.filter(access=1)
            
    for meth in meths:
        meth.access.add(request.user)
        meth.save()
    crits = Criterias.objects.filter(access=1)
    for crit in crits:
        crit.access.add(request.user)
        crit.save()

    return redirect('main:main')

def add_crit(request):
    error= ''

    if request.method =='POST':
        values =dict(request.POST.lists())
        access = []
        access.append(request.user)
        crit_data = {
            'name': values['name'][0],
            'access': access
        }

        crit_form = CriteriaForm(crit_data)

        if crit_form.is_valid():
            crit_form.save()
            crit = Criterias.objects.latest('pk')
            for i in range(0, 3):
                opt_data = {
                    'criteria': crit,
                    'description': values['description'][i]
                }
                opt_form = OptionsForm(opt_data)

                if opt_form.is_valid():
                    opt_form.save()
                else:
                    error = "Ошибка"
            return redirect(reverse('settings:add_scores', kwargs={'pk': Criterias.objects.latest('pk').pk}))

        else:
            error = "Ошибка"

    crit_form = CriteriaForm()
    opt_form = OptionsForm()
    context = {
        'crit_form': crit_form,
        'opt_form': opt_form,
        'error': error,
        'title': "Добавить критерий",
        'title2': "Добавить опции критерия",
        'btn': "Сохранить"
    }
    return render(request, 'settings/add_crit.html', context)

class CritUpdate(UpdateView):
    model = Criterias
    template_name = 'settings/add_crit.html'

    form_class = CriteriaForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ref = self.get_object().pk
        options = [opts.description for opts in list(Options.objects.filter(criteria=ref))]

        for i in range(0, 3):
            opt_data = {
            'description': options[i]
            }
            context[f'option{i+1}'] = OptionsForm(opt_data)     
        context['title'] = "Редактирование критерия"  
        context['title2'] = "Редактировать опции"  
        context['btn'] = "Сохранить"   
        return context
    
    def post(self, request, **kwargs):
        self.id = self.get_object().pk
        crit = Criterias.objects.get(pk=self.id)
        data = dict(request.POST.lists())

        users =  list(self.get_object().access.all())
        access = []

        if len(users) > 1:
            access.append(request.user)
        else:
            access = users
        
        crit_data = {
            'name': data['name'][0],
            'access': access
        }

        if len(users) > 1:
            crit_form = CriteriaForm(crit_data)
            self.get_object().access.remove(request.user)
        else:
            crit_form = CriteriaForm(crit_data, instance=crit)
        
        if crit_form.is_valid():
            new_crit = crit_form.save()
            options = [opts for opts in list(Options.objects.filter(criteria=self.id))]
            for i in range(0,3):
                desc = data['description'][i]
                opt_data = {
                    'criteria': new_crit,
                    'description': desc
                }

                if len(users) > 1:
                    opt_form = OptionsForm(opt_data)

                else:
                    opt_form = OptionsForm(opt_data, instance=options[i])

                if opt_form.is_valid():
                    opt = opt_form.save()

                    scores = list(Scores.objects.filter(option=options[i]))
                    for score in scores:
                        score_data = {
                            'methodology': score.methodology,
                            'option': opt,
                            'score': score.score
                        }

                        form = ScoresForm(score_data)

                        if form.is_valid():
                            form.save()
                else:
                    error = "Ошибка"

            for prior in list(CriteriasPriority.objects.all()):
                if prior.criteria == self.get_object():
                    CriteriasPriority.objects.create(criteria=new_crit, _criteria = prior._criteria, priority=prior.priority)
                elif prior._criteria == self.get_object():
                    CriteriasPriority.objects.create(criteria=prior.criteria, _criteria = new_crit, priority=prior.priority)

            return redirect(reverse('settings:edit_scores', kwargs={'pk': new_crit.pk}))
    

class CritDelete(DeleteView):
    model = Criterias
    success_url = '/settings/'
    template_name = 'settings/add_crit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ref = self.get_object().pk
        name = self.get_object().name
        data = {
            'name': name
        }
        form = CriteriaForm(data)
        context['form'] = form
        options = [opts.description for opts in list(Options.objects.filter(criteria=ref))]

        for i in range(0, 3):
            opt_data = {
            'description': options[i]
            }
            context[f'option{i+1}'] = OptionsForm(opt_data)       
        context['title'] = "Удалить критерий?"  
        context['title2'] = "Будут удалены опции:"  
        context['btn'] = "Удалить"   
        return context
    
    def post(self, request, **kwargs):
        users =  list(self.get_object().access.all())

        if len(users) > 1:
            self.get_object().access.remove(request.user)
        else:
            self.get_object().delete()

        return redirect("settings:settings")

class AddScores(DetailView):
    model = Criterias
    template_name = 'settings/add_scores.html'
    meths_name = [meth.name for meth in list(Methodologies.objects.all())]
    meths = [meth for meth in list(Methodologies.objects.all())]  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opt_pk = self.get_object().pk
        options = [opts.description for opts in list(Options.objects.filter(criteria=opt_pk))]

        for i in range(0, 3):
            context[f'option{i+1}'] = options[i]  
        context['form'] = ScoresForm()   
        context['meths'] = self.meths_name   
        return context

    def post(self, request, **kwargs):
        values = dict(request.POST.lists())

        opt_pk = self.get_object().pk
        options = [opts for opts in list(Options.objects.filter(criteria=opt_pk))]

        i = 0
        for opt in options:
            for meth in self.meths:
                
                score_data = {
                    'option': opt.pk,
                    'methodology': meth.pk,
                    'score': int(values['score'][i])
                }

                i = i + 1

                score_form = ScoresForm(score_data)
                if score_form.is_valid():
                    score_form.save()

                else:
                    error = "Ошибка"

        return redirect(reverse('settings:add_priorities', kwargs={'pk': opt_pk}))
     
class AddPriorities(DetailView):
    model = Criterias
    template_name = 'settings/add_priorities.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        criterias = [crit for crit in list(Criterias.objects.all().exclude(pk=self.get_object().pk))]  
        criterias_names = [crit.name for crit in criterias] 
        new_crit = self.get_object().name
        context['title'] = "Добавление приоритетов"
        context['new'] = new_crit
        context['form'] = PrioritiesForm()   
        context['criterias'] = criterias_names
        return context

    def post(self, request, **kwargs):
        values = request.POST.getlist('priority')
        criterias = [crit for crit in list(Criterias.objects.all().exclude(pk=self.get_object().pk))]
        new_crit = self.get_object()
        i=0
        for crit in criterias:
            val = float(values[i])
            if val in [1, 2, 3, 4, 5]:
                prior_data = {
                    'criteria': new_crit,
                    '_criteria': crit,
                    'priority': val
                }

            else:
                val = val**-1
                prior_data = {
                    'criteria': crit,
                    '_criteria': new_crit,
                    'priority': val
                }  

            if prior_form.is_valid():
                    prior_form.save()
            else:
                error = "Error2"
            i=i+1

        val=1.0
        prior_data = {
                    'criteria': new_crit,
                    '_criteria': new_crit,
                    'priority': val
                }  
        prior_form = PrioritiesForm(prior_data)

        if prior_form.is_valid():
                prior_form.save()
        else:
            error = "Ошибка"

        return redirect('settings:settings')
    
class UpdateScores(UpdateView):
    model = Criterias
    template_name = 'settings/edit_scores.html'
    form_class = ScoresForm
    meths = [meth for meth in list(Methodologies.objects.all())]  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opt_pk = self.get_object().pk
        options = [opts for opts in list(Options.objects.filter(criteria=opt_pk))]
        context['meths'] = self.meths
        forms = []
        for i in range(0, 3):
            context[f'option{i+1}'] = options[i] 
            for meth in self.meths:
                score = Scores.objects.filter(methodology = meth.pk).filter(option=options[i].pk)[0]
                data = {
                    'methodology': meth.name,
                    'score':score
                }
                form = ScoresForm(data)
                forms.append(form)
               
            context[f'forms{i+1}'] = forms
            forms = []      
  
        return context

    def post(self, request, **kwargs):
        values = dict(request.POST.lists())

        opt_pk = self.get_object().pk
        options = [opts for opts in list(Options.objects.filter(criteria=opt_pk))]
        j=0
        for i in range(0, 3):
            for meth in self.meths:
                score = Scores.objects.filter(methodology = meth.pk).filter(option=options[i].pk)
                data = {
                    'option':options[i],
                    'methodology': meth,
                    'score':values['score'][j]
                }
                j=j+1
                score_form = ScoresForm(data, instance=score.first())
                if score_form.is_valid():
                    score_form.save()
                else:
                    error = "Ошибка"

        return redirect('settings:settings')

class UpdateWeights(UpdateView):
    model = Criterias
    template_name = 'settings/add_priorities.html'

    form_class = PrioritiesForm
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        criterias = [crit for crit in list(Criterias.objects.filter(access=self.request.user).exclude(pk=self.get_object().pk))]  

        criterias_names = [crit.name for crit in criterias] 
        new_crit = self.get_object().name
        context['new'] = new_crit
        context['criterias'] = criterias_names

        forms = []
        for crit in criterias:
            form = []
            try:
                obj = list(CriteriasPriority.objects.filter(criteria=self.get_object(), _criteria=crit))[0]
                priority = obj.priority
                data = {
                    'criteria': self.get_object().pk,
                    '_criteria': crit.pk,
                    'priority': priority
                }
            except:
                obj = list(CriteriasPriority.objects.filter(_criteria=self.get_object(), criteria=crit))[0]
                priority = float(obj.priority**-1)
                data = {
                    'criteria': crit.pk,
                    '_criteria': self.get_object().pk,
                    'priority': priority
                }
            form = [self.get_object().name, crit.name, PrioritiesForm(data)]
            forms.append(form)
        context['forms'] = forms 
        context['title'] = "Редактирование приоритетов" 
        return context

    def post(self, request, **kwargs):
        values = request.POST.getlist('priority')
        users =  list(self.get_object().access.all())
        access = []

        if len(users) > 1:
            self.get_object().access.remove(request.user)
            access.append(request.user)
            data = {
                'name':self.get_object().name,
                'access': access
            }
            form = CriteriaForm(data)
            new_crit = form.save()

            for prior in list(CriteriasPriority.objects.all()):
                if prior.criteria ==  self.get_object().pk:
                    CriteriasPriority.objects.create(criteria=new_crit.pk, _criteria = prior._criteria, priority=prior.priority)
                elif prior._criteria ==  self.get_object().pk:
                    CriteriasPriority.objects.create(criteria=prior.criteria, _criteria = new_crit.pk, priority=prior.priority)
            
        else:
            access = users
            new_crit = self.get_object()

        criterias = [crit for crit in list(Criterias.objects.filter(access=request.user).exclude(pk=new_crit.pk))]

        i=0
        for crit in criterias:                
            val = float(values[i])
            if crit == new_crit:
                val=1.0
            if val in [1.0, 2.0, 3.0, 4.0, 5.0]:
                prior_data = {
                    'criteria': new_crit,
                    '_criteria': crit,
                    'priority': val
                }
            else:
                val = val**-1
                prior_data = {
                    'criteria': crit,
                    '_criteria': new_crit,
                    'priority': val
                } 

            prior_form = PrioritiesForm(prior_data)

            if prior_form.is_valid():
                    prior_form.save()
            else:
                error = "Error2"
            i=i+1

        return redirect('settings:settings')
    

class AddScoresMeth(DetailView):
    model = Methodologies
    template_name = 'settings/add_scores_meth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        criterias = list(Criterias.objects.filter(access=self.request.user))

        opts = []
        for crit in criterias:
            options = list(Options.objects.filter(criteria=crit.pk))
            for opt in options:
                el = []
                el.append(opt)
                el.append(ScoresForm())
                opts.append(el)

        context['options'] = opts 
        context['meth'] = self.get_object().name  
        return context

    def post(self, request, **kwargs):
        values = dict(request.POST.lists())

        criterias = list(Criterias.objects.filter(access=self.request.user))
        meth = self.get_object().pk
        i = 0
        for crit in criterias:
            options = list(Options.objects.filter(criteria=crit.pk))
            for opt in options:
                score_data = {
                    'option': opt.pk,
                    'methodology': meth,
                    'score': int(values['score'][i])
                }
                i = i + 1
                score_form = ScoresForm(score_data)
                
                if score_form.is_valid():
                    score_form.save()

                else:
                    error = "Ошибка"

        return redirect('settings:settings')
    
class UpdateScoresMeth(UpdateView):
    model = Methodologies
    template_name = 'settings/add_scores_meth.html'
    form_class = ScoresForm 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        criterias = list(Criterias.objects.filter(access=self.request.user))
        meth = self.get_object().pk

        opts = []
        for crit in criterias:
            options = list(Options.objects.filter(criteria=crit.pk))
            for opt in options:
                el = []
                el.append(opt)
                score = Scores.objects.get(option=opt.pk, methodology=meth)
                score_data = {
                    'option': opt.pk,
                    'methodology': meth,
                    'score': score.score
                }
                form =  ScoresForm(score_data)  
                el.append(form)
                opts.append(el)

        context['options'] = opts 
        context['meth'] = self.get_object().name  
        return context

    def post(self, request, **kwargs):
        values = dict(request.POST.lists())

        criterias = list(Criterias.objects.filter(access=self.request.user))
        meth = self.get_object().pk
        i = 0
        for crit in criterias:
            options = list(Options.objects.filter(criteria=crit.pk))
            for opt in options:
                score_data = {
                    'option': opt.pk,
                    'methodology': meth,
                    'score': int(values['score'][i])
                }
                i = i + 1
                score = Scores.objects.get(option=opt.pk, methodology=meth)
                score_form = ScoresForm(score_data, instance=score)
                
                if score_form.is_valid():
                    score_form.save()

                else:
                    error = "Ошибка"

        return redirect('settings:settings')