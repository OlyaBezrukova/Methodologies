# from .models import Methodologies, Criterias, Options, Scores, CriteriasPriority
# from django.forms import ModelForm, TextInput, IntegerField, NumberInput, Select, Textarea

# class MethodologyForm(ModelForm):
#     class Meta:
#         model = Methodologies
#         fields = ['name']

#         widgets = {
#             "name": TextInput(attrs={
#                 'class': 'meth_form',
#                 'placeholder': 'Input name'
#             })
#         }

# class CriteriaForm(ModelForm):
#     class Meta:
#         model = Criterias
#         fields = ['name']

#         widgets = {
#             "name": TextInput(attrs={
#                 'class': 'crit_form',
#                 'placeholder': 'Input name'
#             })
#         }

# class OptionsForm(ModelForm):
#     class Meta:
#         model = Options
#         fields = ['criteria', 'description']

#         widgets = {
#             "description": Textarea(attrs={
#                 'class': 'opt_form',
#                 'placeholder': 'Input option',
#                 'style': 'width:700px; height:100px'
#             })
#         }

# class ScoresForm(ModelForm):
#     class Meta:
#         model = Scores
#         fields = ['option', 'methodology', 'score']

#         widgets = {
#             "methodology": TextInput(attrs={
#                 'readonly': True,
#                 'class': 'meth_form',
#                 'placeholder': 'Input option'
#             }),
#             "score": NumberInput(attrs={
#                 'class': 'score_form',
#                 'placeholder': 'Input score'
#             })
#         }

# class PrioritiesForm(ModelForm):
#     class Meta:
#         model = CriteriasPriority
#         fields = ['criteria', '_criteria', 'priority']

#         widgets = {
#             "criteria": TextInput(attrs={
#                 'readonly': True,
#                 'class': 'meth_form',
#                 'placeholder': 'Input option'
#             }),
#             "_criteria": TextInput(attrs={
#                 'readonly': True,
#                 'class': 'meth_form',
#                 'placeholder': 'Input option'
#             }),
#             "priority": Select(attrs={
#                 'class': 'description_form',
#                 'placeholder': 'Input priority',
#                 'style': 'width:250px'
#             }, choices=(
#                 (1.0, "1"), #Критерии равнозначны
#                 (2.0, "2"), #Первый критерий имеет незначительно большую значимость, чем второй
#                 (3.0, "3"),
#                 (4.0, "4"),
#                 (5.0, "5"),
#                 (1/2, "1/2"),
#                 (1/3, "1/3"),
#                 (1/4, "1/4"),
#                 (1/5, "1/5")
#             ))
#         }


