from django.urls import path
from .views import *

urlpatterns = [
    path('question/', question_list, name='question-list'),
    path('question/<int:id>/', question_detail, name='question-detail')
]