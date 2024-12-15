
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from vocabularies.serializers import VocabularySerializer,WordSerializer
from django.shortcuts import get_object_or_404
from profiles.models import Profile
from vocabularies.models import Vocabulary,Word
from vocabularies.permissions import IsOwnerOrReadOnly,IsOwnerOfVocabularyOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class VocabularyListCreateView(ListCreateAPIView):
    serializer_class=VocabularySerializer
    
    def get_queryset(self):
        profile_id=self.request.query_params.get('profile_id')

        if profile_id:
            profile=get_object_or_404(Profile,id=profile_id)
        else:
            profile=self.request.user.profile   # get_object_or_404(Profile,user=self.request.user) #

        queryset=Vocabulary.objects.filter(profile=profile)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class VocabularyDetailView(RetrieveUpdateDestroyAPIView):
    queryset=Vocabulary.objects.all()
    serializer_class=VocabularySerializer
    permission_classes=[IsAuthenticated,IsOwnerOrReadOnly]
    lookup_field='id'

class WordListCreateView(ListCreateAPIView):
    serializer_class=WordSerializer

    def get_queryset(self):
        vocabulary_id=self.kwargs.get('vocabulary_id')
        vocabulary=get_object_or_404(Vocabulary,id=vocabulary_id)

        return Word.objects.filter(vocabulary=vocabulary)
    
    def perform_create(self, serializer):
        vocabulary_id=self.kwargs.get('vocabulary_id')
        vocabulary=get_object_or_404(Vocabulary,id=vocabulary_id,profile=self.request.user.profile)
        serializer.save(vocabulary=vocabulary)

class WordDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class=WordSerializer
    queryset=Word.objects.all()
    
    permission_classes=[IsAuthenticated,IsOwnerOfVocabularyOrReadOnly]
    
    def get_object(self):
        vocabulary_id=self.kwargs.get('vocabulary_id')
        word_id=self.kwargs.get('word_id')

        word=get_object_or_404(Word,id=word_id,vocabulary_id=vocabulary_id)
        self.check_object_permissions(self.request,word)
        return word

class CopyVocabularyView(APIView):

    def post(self, request,vocabulary_id):
        original_vocabulary=get_object_or_404(Vocabulary,id=vocabulary_id)

        copied_vocabulary=Vocabulary.objects.create(
            profile=request.user.profile,
            name=f"Copy of {original_vocabulary.name}",
            description=original_vocabulary.description,
        )

        words=Word.objects.filter(vocabulary=original_vocabulary)
        for word in words:
            Word.objects.create(
                vocabulary=copied_vocabulary,
                text=word.text,
                meaning=word.meaning,
                example_sentence=word.example_sentence
            )

        return Response({
            "success":"vocabulary copied successfully!"
        })
    
