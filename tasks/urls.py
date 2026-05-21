from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('tarea/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tarea/nueva/', views.TaskCreateView.as_view(), name='task_create'),
    path('tarea/<int:pk>/editar/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tarea/<int:pk>/eliminar/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('tarea/<int:pk>/toggle/', views.task_toggle, name='task_toggle'),
]
