from django.urls import path
from .views import *

urlpatterns = [
    path('question/', QuestionList.as_view(), name='question-list'),
    path('question/<int:pk>/', QuestionDetail.as_view(), name='question-detail')
    #GenericAPIView에서 아이디를 pk로 가져오기 때문에 id -> pk로 바꿔줌
]