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

    def create(self, request, *args, **kwargs):
        new_data = request.data.copy()
        # user.id로 받은 이유는 딕셔너리 형태의 원시 데이터에선 
        # 사용자의 id를 넣어야 직렬화가 제대로 수행되기 때문.
        new_data['voter'] = request.user.id
        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class VoteDetial(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    # List는 조회는 get_queryset()을 override해서 조회를 조절하고
    # detail은 permissions을 조절해서 authorization 해준다.
    permission_classes = [permissions.IsAuthenticated, IsVoter]

    def perform_update(self, serializer):
        '''voter=self.request.user: 직렬화 후에 
           객체 기반의 데이터로 처리되는 부분에서,
           User 객체 자체를 사용.
           ORM이 자동으로 객체의 ID를 처리해줌.
        '''
        serializer.save(voter=self.request.user)


        
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
    
