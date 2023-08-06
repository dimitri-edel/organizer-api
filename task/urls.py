from django.urls import path
from . import views


urlpatterns = [
    path('task/', views.TaskList.as_view()),
    path('task/<int:pk>', views.TaskDetails.as_view()),   
]