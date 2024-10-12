from polls.models import Question
from polls_api.serializers import QuestionSerializer
from rest_framework import generics

#ListCreateAPIView는 mixin의 list와 create를 상속받음.
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()    #GenericAPIView 에서 기능 제공
    serializer_class = QuestionSerializer  #GenericAPIView 에서 기능 제공

    #get,과 post가 ListCreateAPIView에 구현되어있음.

#RetrieveModelMixin 은 1개를 get
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
