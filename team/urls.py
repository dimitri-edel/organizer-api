from django.urls import path
from team import views

urlpatterns = [
    path('team/', views.TeamList.as_view()),
    path('team/<int:pk>/', views.TeamDetails.as_view()),
     path('teammates/', views.TeamMates.as_view()),
    path('membership/', views.TeamMembershipList.as_view()),
    path('membership/<int:pk>', views.TeamMembershipDetails.as_view()),
    path('leave/team/<int:team_id>', views.LeaveTeam.as_view()),
]