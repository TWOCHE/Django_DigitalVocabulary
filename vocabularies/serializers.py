from rest_framework import serializers
from vocabularies.models import Vocabulary,Word

class VocabularySerializer(serializers.ModelSerializer):

    class Meta:
        model=Vocabulary
        fields=('id','name','description')

class WordSerializer(serializers.ModelSerializer):
    vocabulary=serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model=Word
        fields='__all__'