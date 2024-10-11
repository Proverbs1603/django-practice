from django.urls import path
from .views import *

urlpatterns = [
    path('question/', QuestionList.as_view(), name='question-list'),
    path('question/<int:id>/', QuestionDetail.as_view(), name='question-detail')
]