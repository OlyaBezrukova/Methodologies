from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Prefetch


class Criterias(models.Model):
    name = models.CharField('Критерий', max_length=100)
    access = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/settings'
    
    class Meta:
        verbose_name  = 'Criteria'
        verbose_name_plural  = 'Criterias'


class Options(models.Model):
    criteria = models.ForeignKey('Criterias', on_delete=models.CASCADE)
    description = models.TextField('Описание варианта ответа', unique=False)

    def __str__(self):
        return self.description
    
    def get_absolute_url(self):
        return '/settings'
    
    class Meta:
        verbose_name  = 'Options'
        verbose_name_plural  = 'Options'

class Methodologies(models.Model):
    name = models.CharField('Название методологии', max_length=100)
    access = models.ManyToManyField(User)

    def get_absolute_url(self):
        return '/settings'
    
    def __str__(self):
        return self.name
    

class Scores(models.Model):
    option = models.ForeignKey('Options', on_delete=models.CASCADE)
    methodology = models.ForeignKey('Methodologies', on_delete=models.CASCADE)
    score = models.IntegerField('Score')

    class Meta:
        verbose_name = 'Scores'
        verbose_name_plural = 'Scores'

    def __str__(self):
        # return f"{str(self.option)} - {str(self.methodology)} - {str(self.score)}"
        return str(self.score)
    
class CriteriasPriority(models.Model):
    criteria = models.ForeignKey('Criterias', related_name="first", on_delete=models.CASCADE, null=True)
    _criteria = models.ForeignKey('Criterias', related_name="second", on_delete=models.CASCADE, null=True)  
    priority = models.FloatField('Priority')

    class Meta:
        verbose_name = 'Priority'
        verbose_name_plural = 'Priorities'

    def __str__(self):
        return f"{str(self.criteria)} - {str(self._criteria)} - {str(self.priority)}"
        


    
