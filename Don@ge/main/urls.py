
from django.urls import path 
from . import views


urlpatterns = [
     path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/complete/<int:task_id>/',views.complete_task,name='complete_task'),
    path('tasks/delete/<int:task_id>/',views.delete_task,name='delete_task'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/update/<int:item_id>/', views.update_inventory, name='update_inventory'),
    path('inventory/delete/<int:item_id>/', views.delete_inventory, name='delete_inventory'),
    ]
 