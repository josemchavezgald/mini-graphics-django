from django.urls import path
from . import views
 
urlpatterns = [
    path("", views.home_index, name="home_index"),
    path('dashboard', views.dashboard_index,name="dashboard_index"),
    path('updateDashboard/',views.dashboard_change, name="dashboard_change")
     # path("<int:pk>/", views.project_detail, name="project_detail"),
]
