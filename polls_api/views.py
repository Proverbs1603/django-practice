from polls.models import Question, Vote
from polls_api.serializers import QuestionSerializer, UserSerializer, RegisterSerializer, VoteSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly, IsVoter

class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    #내가 만든 Vote만 봐야함 (현재 접속한 user가 voter가 같은것), queryset = 
    def get_queryset(self, *args, **kwargs):
        return Vote.objects.filter(voter=self.request.user)

    #현재 로그인 되어있는 사용자로 voter 지정
    def perform_create(self, serializer):
        serializer.save(voter=self.request.user)

class VoteDetial(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    # List는 조회는 get_queryset()을 override해서 조회를 조절하고
    # detail은 permissions을 조절해서 authorization 해준다.
    permission_classes = [permissions.IsAuthenticated, IsVoter]


        
#ListCreateAPIView는 mixin의 list와 create를 상속받음.
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()    #GenericAPIView 에서 기능 제공
    serializer_class = QuestionSerializer  #GenericAPIView 에서 기능 제공
    #로그인된 사용자는 모든 요청을 할 수 있지만, **로그인되지 않은 사용자(익명 사용자)**는 읽기 전용 요청만 할 수 있다는 의미
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        #create 할 때는 이미 지정된 사용자를 owner로 사용한다는 의미
        # QuestionSerializer에서 owner 필드는 ReadOnlyField 인데 어떻게 수정이되나?
        # save() 메서드는 제약사항 없이 동작이 가능함. 
        return serializer.save(owner=self.request.user)

#RetrieveModelMixin 은 1개를 get
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#사용자는 만들기만하고 조회는 안되게
class RegisterUser(generics.CreateAPIView):
    #queryset을 줄 필요 없다.
    serializer_class = RegisterSerializer
    
