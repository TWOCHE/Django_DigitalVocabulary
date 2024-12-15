from django.urls import path
from exercises.views import QuestionView


urlpatterns=[
    path('question/',QuestionView.as_view(),name='create-question'),

]