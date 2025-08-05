from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Note
from .serializers import Note_Serializer
from .services import GrammarCheck
from django.core.files import File
import os
import markdown2
from django.http import HttpResponse, Http404

# Create your views here.

class NoteRenderedView(APIView):
    def get_object(self, pk, user):
        try:
            return Note.objects.get(pk=pk, author=user)
        except Note.DoesNotExist:
            raise Http404("Note not found.") 
        
    def get(self, request, pk=None):
        note = self.get_object(pk, request.user)
        if not note.md_file:
            return HttpResponse("No file to render.", status=status.HTTP_400_BAD_REQUEST)
        
        with open (note.md_file.path, "r",encoding="utf-8") as f:
            markdown_content = f.read()

        html_content = markdown2.markdown(markdown_content)
        return HttpResponse(html_content, content_type='text/html')



class Notes(APIView):
    
    def get_object(self, pk, user):
        try:
                return Note.objects.get(pk=pk, author=user)
        except Note.DoesNotExist:
                return None

    def get(self, request, pk=None):
        errors = []

        if pk:
            note = self.get_object(pk, request.user)
            if not note:
                    return Response({'Error' : "Note can't be found."}, status=status.HTTP_404_NOT_FOUND)
            if note.text:
                checker = GrammarCheck(text=note.text)
            elif note.md_file:
                checker = GrammarCheck(filepath=note.md_file.path)
            errors = checker.check()
            serializer = Note_Serializer(note)
            return Response({
                            "note": serializer.data,
                            "grammar_errors": errors
                        }, status=status.HTTP_200_OK)

        notes = Note.objects.filter(author=request.user)
        serializer = Note_Serializer(notes, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = Note_Serializer(data = request.data)
        if serializer.is_valid():
            serializer.save(author = request.user)
            note = serializer.instance
            if note.text:
                file_name = f"note_{note.pk}_{note.author.id}.md"
                file_path = f"media/temp/{file_name}"
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                with open(file_path, "w", encoding="utf-8") as f:
                     f.write(note.text)

                with open(file_path, "rb") as f:
                     django_file = File(f)
                     note.md_file.save(file_name, django_file, save=True)   
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        note = self.get_object(pk, request.user)
        serializer = Note_Serializer(note, data = request.data)

        if serializer.is_valid():
            serializer.save()
            note = serializer.instance

            if note.text:
                if note.md_file:
                     note.md_file.delete(save=False)
                file_name = f"note_{note.pk}_{note.author.id}.md"
                file_path = f"media/temp/{file_name}"
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                with open(file_path, "w", encoding="utf-8") as f:
                     f.write(note.text)

                with open(file_path, "rb") as f:
                     django_file = File(f)
                     note.md_file.save(file_name, django_file, save=True)
                checker = GrammarCheck(text=note.text)
            elif note.md_file:
                checker = GrammarCheck(filepath=note.md_file.path)
            errors = checker.check()
            return Response({
                            "note": serializer.data,
                            "grammar_errors": errors
                            }, status=status.HTTP_200_OK)

    
    def delete(self, request, pk):
        note = self.get_object(pk, request.user)
        if not note:
            return Response({'error': 'Note not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if note.md_file:
            note.md_file.delete(save=False)

        note.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


