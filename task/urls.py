from django.urls import path
from .views import TaskListCreateView, TaskGetUpdateDeleteView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:pk>/', TaskGetUpdateDeleteView.as_view(), name='task-get-update-delete'),
]
