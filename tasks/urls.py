from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import TaskListCreateView, TaskDetailView, CategoryListCreateView, CategoryDetailView


urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]