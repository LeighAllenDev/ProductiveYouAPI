from django.contrib import admin
from .models import Task, Category, TaskFile

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'is_urgent', 'due_date', 'category', 'team')
    list_filter = ('is_urgent', 'due_date', 'category', 'team')
    search_fields = ('task_name', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(TaskFile)
class TaskFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    search_fields = ('file',)