from rest_framework import serializers
from polls.models import Question
from django.contrib.auth.models import User

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

    '''
    serializers.Serializer 가 아니라 serializers.ModelSerializer 를 상속하면 아래 코드를 작성하지 않아도 됨.

    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.question_text = validated_data.get('question_text', instance.question_text) + '[시리얼라이저에서 업데이트]'
        instance.save()
        return instance
    '''