from django.urls import path
from .views import TeamListCreateView, TeamDetailView

urlpatterns = [
    path('teams/', TeamListCreateView.as_view(), name='team-list-create'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
]