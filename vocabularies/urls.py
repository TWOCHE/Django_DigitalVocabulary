from django.urls import path
from vocabularies.views import VocabularyListCreateView,VocabularyDetailView,WordListCreateView,WordDetailView,CopyVocabularyView

urlpatterns=[
    path('',VocabularyListCreateView.as_view(),name='vocabularies'),
    path('<int:id>/',VocabularyDetailView.as_view(),name='vocabulary-detail'),
    path('<int:vocabulary_id>/words/',WordListCreateView.as_view(),name='words'),
    path('<int:vocabulary_id>/words/<int:word_id>/',WordDetailView.as_view(),name='word-detail'),
    path('<int:vocabulary_id>/copy/',CopyVocabularyView.as_view(),name='copy-vocabulary')

]