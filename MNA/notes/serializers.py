from rest_framework import serializers
from .models import Note
import markdown2

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['owner']

class RenderedNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['id', 'title', 'rendered.html']

    def get_rendered_html(self, obj):
        return markdown2.markdown(obj.content or " ")