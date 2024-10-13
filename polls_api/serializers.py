from rest_framework import serializers
from polls.models import Question, Choice, Vote
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueTogetherValidator

class VoteSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['choice'].question.id != attrs['question'].id:
            raise serializers.ValidationError("Question과 Choice가 조합이 맞지 않습니다.")
        
        return attrs
    
    class Meta:
        model = Vote
        fields = ['id', 'question', 'choice', 'voter']
        validators = [
            UniqueTogetherValidator(
                queryset=Vote.objects.all(),
                fields=['question', 'voter']
            )
        ]

class ChoiceSerializer(serializers.ModelSerializer): 
    #메서드로 필드값을 수정해서 불러온다.
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ['choice_text', 'votes_count']
    
    #get_필드명이 default 메소드명 , obj는 직렬화 중인 Choice 인스턴스
    def get_votes_count(self, obj):
        #vote_set중에 choice_id가 해당 인스턴스인 것의 개수 return 
        return obj.vote_set.count()

class QuestionSerializer(serializers.ModelSerializer):
    #owner의 username으로 보임
    owner = serializers.ReadOnlyField(source='owner.username')
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'owner', 'choices']
    
class UserSerializer(serializers.ModelSerializer):
    #question은 user 모델에 있는 필드가 아니기 때문에 아래와 별도로 설정을 해주어야함.
    #questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    #questions = serializers.StringRelatedField(many=True, read_only=True)
    #questions = serializers.SlugRelatedField(many=True, read_only=True, slug_field='pub_date')
    questions = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='question-detail')
    
    class Meta:
        model = User
        fields = ['id', 'username', 'questions', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    #write_only, required, validators 등의 옵션을 주기위해 별도로 작성
    #write_only로 password는 조회가 안되도록
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        #사용자가 입력한 값인 attrs 딕셔너리에서 password와 password2를 비교
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "두 패스워드가 일치하지 않습니다."})
        return attrs
    
    def create(self, validated_data):
        #원래 User에는 password2라는 field는 없어서 user를 다시 create해서 사용함.
        user = User.objects.create(username=validated_data['username'])
        #비밀번호를 **해싱(hash)**하여 저장하기 위해 set_password() 쓰기.
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    class Meta:
        model = User
        fields = ['username', 'password','password2']