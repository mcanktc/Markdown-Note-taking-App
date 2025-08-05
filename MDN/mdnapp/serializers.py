from rest_framework import serializers
from .models import Note

class Note_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'text', 'author', 'md_file', 'take_type']
        read_only_fields = ['author']

    def validate(self, data):
        if data.get("take_type") == 'T':
            if data.get('text') == None:
                raise serializers.ValidationError({'error' : 'Lütfen bir not yazınız.'})
            return data
        elif data.get('take_type') == 'F':
            if data.get('md_file') == None:
                raise serializers.ValidationError({'error' : 'Lütfen bir dosya yükleyiniz.'})
            return data