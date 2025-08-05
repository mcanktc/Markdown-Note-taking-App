from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.Notes.as_view(), name='notes'),
    path('notes/<int:pk>/', views.Notes.as_view(), name='note-detail'),
    path('notes/<int:pk>/detail', views.NoteRenderedView.as_view(), name='note')
]