from django.urls import path
from team import views

urlpatterns = [
    path('team/', views.TeamList.as_view()),
    path('team/<int:pk>/', views.TeamDetails.as_view()),
]