from rest_framework import generics, permissions, status
from rest_framework.response import Response
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
        return Task.objects.filter(team__in=user_teams).order_by('-id')

    def perform_create(self, serializer):
        task = serializer.save(owner=self.request.user)

        files_data = self.request.FILES.getlist('files')
        for file_data in files_data:
            task_file = TaskFile.objects.create(file=file_data)
            task.files.add(task_file)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def update(self, request, *args, **kwargs):
        """
        Override to allow marking tasks as complete/incomplete only
        for team members.
        """
        instance = self.get_object()

        if instance.team and request.user.profile in instance.team.users.all():
            if 'completed' in request.data:
                instance.completed = request.data['completed']
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)

        if instance.owner != request.user:
            return Response(
                {"detail": "You do not have permission to edit this task."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)


class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
