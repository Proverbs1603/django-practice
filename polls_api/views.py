from rest_framework.decorators import api_view
from polls.models import Question
from polls_api.serializers import QuestionSerializer
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView 

#ListModelMixin 은 list를 get, CreateModelMixin 은 create
class QuestionList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Question.objects.all()    #GenericAPIView 에서 기능 제공
    serializer_class = QuestionSerializer  #GenericAPIView 에서 기능 제공

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)    

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)  #검증 후 생성 로직이 다 구현되어있음.
    
#RetrieveModelMixin 은 1개를 get
class QuestionDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
        
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        


