from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import Task, TaskFile, Category
from .serializers import TaskSerializer, TaskFileSerializer, CategorySerializer
from productive_you_api.permissions import IsOwnerOrReadOnly

class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile  # Retrieve user's profile
            user_teams = profile.teams.all()  # Retrieve teams associated with the profile
            tasks = Task.objects.filter(team__in=user_teams)
            serializer = TaskSerializer(tasks, many=True, context={'request': request})
            return Response(serializer.data)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist for this user.")

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            profile = request.user.profile
            task = serializer.save(team=profile.teams.first())  # Example: Assign first team from user's profile

            # Handle file uploads
            files_data = request.FILES.getlist('files')
            for file_data in files_data:
                task_file = TaskFile.objects.create(file=file_data)
                task.files.add(task_file)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        # Handle file uploads on update
        files_data = self.request.FILES.getlist('files')
        if files_data:
            instance = serializer.instance
            instance.files.clear()  # Clear existing files if new files are provided
            for file_data in files_data:
                task_file = TaskFile.objects.create(file=file_data)
                instance.files.add(task_file)
        
        serializer.save()

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.files.all().delete()  # Delete associated files before deleting task
        return super().delete(request, *args, **kwargs)

class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
