from django.urls import path
from .views import todo_list, todo_create, todo_update, todo_delete

urlpatterns = [
    path('', todo_list, name='todo_list'),
    path('todo/new/', todo_create, name='todo_create'),
    path('todo/<int:index>/edit/', todo_update, name='todo_update'),
    path('todo/<int:index>/delete/', todo_delete, name='todo_delete'),
]
