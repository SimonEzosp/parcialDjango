from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from .models import Task
from .forms import TaskForm


class TaskListView(ListView):
    """Lista todas las tareas. Soporta filtros por status y prioridad."""
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        if status == 'completed':
            qs = qs.filter(completed=True)
        elif status == 'pending':
            qs = qs.filter(completed=False)
        if priority in ['low', 'medium', 'high']:
            qs = qs.filter(priority=priority)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total'] = Task.objects.count()
        ctx['completed'] = Task.objects.filter(completed=True).count()
        ctx['pending'] = Task.objects.filter(completed=False).count()
        return ctx


class TaskDetailView(DetailView):
    """Detalle de una tarea."""
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(SuccessMessageMixin, CreateView):
    """Crea una nueva tarea."""
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')
    success_message = 'Tarea "%(title)s" creada exitosamente.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Crear'
        return ctx


class TaskUpdateView(SuccessMessageMixin, UpdateView):
    """Actualiza una tarea existente."""
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')
    success_message = 'Tarea "%(title)s" actualizada.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Editar'
        return ctx


class TaskDeleteView(SuccessMessageMixin, DeleteView):
    """Elimina una tarea con confirmación."""
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    success_message = 'Tarea eliminada correctamente.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


def task_toggle(request, pk):
    """Vista funcional para alternar estado completado/pendiente."""
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    estado = 'completada' if task.completed else 'pendiente'
    messages.info(request, f'Tarea marcada como {estado}.')
    return redirect('task_list')
