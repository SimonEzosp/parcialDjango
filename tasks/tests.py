from django.test import TestCase, Client
from django.urls import reverse
from .models import Task


class TaskModelTest(TestCase):
    """Tests del modelo Task."""

    def setUp(self):
        self.task = Task.objects.create(
            title='Tarea de prueba',
            description='Descripción de prueba',
            priority='high',
            completed=False,
        )

    def test_task_creation(self):
        """El modelo se crea correctamente."""
        self.assertEqual(self.task.title, 'Tarea de prueba')
        self.assertEqual(self.task.priority, 'high')
        self.assertFalse(self.task.completed)

    def test_str_representation(self):
        """__str__ retorna el título."""
        self.assertEqual(str(self.task), 'Tarea de prueba')

    def test_default_priority(self):
        """La prioridad por defecto es 'medium'."""
        task = Task.objects.create(title='Sin prioridad')
        self.assertEqual(task.priority, 'medium')

    def test_default_completed_false(self):
        """Las tareas nuevas están pendientes por defecto."""
        task = Task.objects.create(title='Nueva tarea')
        self.assertFalse(task.completed)

    def test_ordering(self):
        """Las tareas se ordenan por fecha de creación descendente."""
        task2 = Task.objects.create(title='Segunda tarea')
        tasks = list(Task.objects.all())
        self.assertEqual(tasks[0], task2)


class TaskListViewTest(TestCase):
    """Tests de la vista ListView."""

    def setUp(self):
        self.client = Client()
        Task.objects.create(title='Tarea 1', priority='high', completed=False)
        Task.objects.create(title='Tarea 2', priority='low', completed=True)

    def test_list_status_200(self):
        """La lista de tareas responde 200."""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_uses_correct_template(self):
        """Usa el template correcto."""
        response = self.client.get(reverse('task_list'))
        self.assertTemplateUsed(response, 'tasks/task_list.html')

    def test_list_shows_all_tasks(self):
        """Muestra todas las tareas."""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(len(response.context['tasks']), 2)

    def test_filter_by_status_pending(self):
        """Filtrar por pendientes funciona."""
        response = self.client.get(reverse('task_list') + '?status=pending')
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertFalse(response.context['tasks'][0].completed)

    def test_filter_by_status_completed(self):
        """Filtrar por completadas funciona."""
        response = self.client.get(reverse('task_list') + '?status=completed')
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertTrue(response.context['tasks'][0].completed)

    def test_filter_by_priority(self):
        """Filtrar por prioridad funciona."""
        response = self.client.get(reverse('task_list') + '?priority=high')
        self.assertEqual(len(response.context['tasks']), 1)

    def test_context_stats(self):
        """El contexto incluye estadísticas correctas."""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.context['total'], 2)
        self.assertEqual(response.context['pending'], 1)
        self.assertEqual(response.context['completed'], 1)


class TaskDetailViewTest(TestCase):
    """Tests de la vista DetailView."""

    def setUp(self):
        self.task = Task.objects.create(title='Detalle tarea', priority='medium')

    def test_detail_status_200(self):
        response = self.client.get(reverse('task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_404_on_missing(self):
        response = self.client.get(reverse('task_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_detail_context(self):
        response = self.client.get(reverse('task_detail', args=[self.task.pk]))
        self.assertEqual(response.context['task'], self.task)


class TaskCreateViewTest(TestCase):
    """Tests de la vista CreateView."""

    def test_create_get_status_200(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_valid_post(self):
        """POST válido crea la tarea y redirige."""
        response = self.client.post(reverse('task_create'), {
            'title': 'Nueva tarea',
            'description': 'Desc',
            'priority': 'medium',
            'completed': False,
        })
        self.assertRedirects(response, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Nueva tarea')

    def test_create_invalid_post(self):
        """POST inválido (sin título) no crea la tarea."""
        response = self.client.post(reverse('task_create'), {
            'title': '',
            'priority': 'medium',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)


class TaskUpdateViewTest(TestCase):
    """Tests de la vista UpdateView."""

    def setUp(self):
        self.task = Task.objects.create(title='Original', priority='low')

    def test_update_get_status_200(self):
        response = self.client.get(reverse('task_update', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_valid_post(self):
        """POST válido actualiza la tarea."""
        self.client.post(reverse('task_update', args=[self.task.pk]), {
            'title': 'Actualizada',
            'priority': 'high',
            'completed': True,
        })
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Actualizada')
        self.assertEqual(self.task.priority, 'high')
        self.assertTrue(self.task.completed)


class TaskDeleteViewTest(TestCase):
    """Tests de la vista DeleteView."""

    def setUp(self):
        self.task = Task.objects.create(title='A eliminar', priority='low')

    def test_delete_get_status_200(self):
        response = self.client.get(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_post_removes_task(self):
        """POST elimina la tarea y redirige."""
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertRedirects(response, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 0)


class TaskToggleViewTest(TestCase):
    """Tests de la vista funcional toggle."""

    def setUp(self):
        self.task = Task.objects.create(title='Toggle tarea', completed=False)

    def test_toggle_completes_task(self):
        self.client.get(reverse('task_toggle', args=[self.task.pk]))
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

    def test_toggle_twice_returns_pending(self):
        self.client.get(reverse('task_toggle', args=[self.task.pk]))
        self.client.get(reverse('task_toggle', args=[self.task.pk]))
        self.task.refresh_from_db()
        self.assertFalse(self.task.completed)
