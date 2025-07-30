from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .models import Note
from .serializers import NoteSerializer, RenderedNoteSerializer
import language_tool_python


# Create your views here.
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['get'], url_path='rendered')
    def render_markdown(self, request, pk=None):
        note = self.get_object()
        serializer = RenderedNoteSerializer(note)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='check-grammer')
    def check_grammer(self, request, pk=None):
        note = self.get_object()
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(note.content or " ")
        suggestions = [{'message' : m.message, 'context' : m.context} for m in matches]
        return Response({'errors' : suggestions})
