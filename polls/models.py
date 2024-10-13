from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='질문') #verbose는 admin페이지의 나오는 컬럼명
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일') 
    #user.questions.all() 로 user가 가진 모든 question목록 조회 가능
    owner = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE, null=True)
    

    #데코레이터 (boolean을 True로 하면 체크이미지로 보임, description은 admin페이지의 나오는 컬럼명)
    @admin.display(boolean=True, description='최근생성(하루기준)')
    def was_published_recently(self):
        #현재 시간에서 1일을 뺀 시간을 나타냅니다. 즉, 24시간 전의 시간을 구합니다.
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        if self.was_published_recently():
            new_badge = 'NEW!!!'
        else:
            new_badge = ''
        return f'{new_badge}퀴즈제목: {self.question_text}, 날짜: {self.pub_date}'
    
    

class Choice(models.Model):
    #ForeignKey에서 related_name을 정해주지 않으면 django에서 choice_set을 구현해줌.
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'[{self.question.question_text}] : {self.choice_text}'

class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        #제약사항 : 한 유저는 한 질문에 대해 하나의 투표만 할 수 있다.
        constraints = [
            models.UniqueConstraint(fields=['question', 'voter'], name='unique_voter_for_questions')
        ]