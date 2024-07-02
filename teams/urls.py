from django.urls import path
from .views import TeamListCreateView, TeamDetailView, TeamJoinView

urlpatterns = [
    path('', TeamListCreateView.as_view(), name='team-list-create'),
    path('<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
    path('<int:pk>/join/', TeamJoinView.as_view(), name='team-join'),
]