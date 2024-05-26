from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.settings, name='settings'),
    path('add_meth', views.add_meth, name='add_meth'),
    path('<int:pk>/meth_update', views.MethUpdate.as_view(), name='meth_update'),
    path('<int:pk>/meth_delete', views.MethDelete.as_view(), name='meth_delete'),
    path('<int:pk>/add_scores_meth', views.AddScoresMeth.as_view(), name='add_scores_meth'),
    path('<int:pk>/update_scores_meth', views.UpdateScoresMeth.as_view(), name='update_scores_meth'),
    
    path('add_crit', views.add_crit, name='add_crit'),     
    path('<int:pk>/crit_update', views.CritUpdate.as_view(), name='crit_update'),
    path('<int:pk>/crit_delete', views.CritDelete.as_view(), name='crit_delete'), 

    path('<int:pk>/add_scores', views.AddScores.as_view(), name='add_scores'),
    path('<int:pk>/edit_scores', views.UpdateScores.as_view(), name='edit_scores'),

    path('<int:pk>/add_priorities', views.AddPriorities.as_view(), name='add_priorities'),
    
    path('<int:pk>/update_weights', views.UpdateWeights.as_view(), name='update_weights'),
    path('return_base', views.return_base, name='return_base'),
] 
