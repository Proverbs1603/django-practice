from rest_framework import serializers
from polls.models import Question
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date']
    
class UserSerializer(serializers.ModelSerializer):
    #question은 user 모델에 있는 필드가 아니기 때문에 아래와 별도로 설정을 해주어야함.
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())

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