from rest_framework import generics, permissions
from .models import Task, TaskFile, Category
from .serializers import TaskSerializer, CategorySerializer
from productive_you_api.permissions import IsOwnerOrReadOnly
from .pagination import CustomPagination

class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        profile = self.request.user.profile
        user_teams = profile.teams.all()
        return Task.objects.filter(team__in=user_teams)

    def perform_create(self, serializer):
        profile = self.request.user.profile
        task = serializer.save(owner=self.request.user)

        files_data = self.request.FILES.getlist('files')
        for file_data in files_data:
            task_file = TaskFile.objects.create(file=file_data)
            task.files.add(task_file)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
