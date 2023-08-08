from django.urls import path
from . import views


urlpatterns = [
    path('tasks/', views.TaskList.as_view()),
    path('task/<int:pk>', views.TaskDetails.as_view()), 
]