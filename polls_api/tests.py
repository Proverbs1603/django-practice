from django.test import TestCase
from polls_api.serializers import QuestionSerializer, VoteSerializer
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote
from rest_framework.test import APITestCase
from django.urls import reverse #메서드 레벨에서는 reverse-lazy보다 reverse 쓴다.
from rest_framework import status
from django.utils import timezone

class QuestionListTest(APITestCase):
    def setUp(self):
        self.question_data = {'question_text': 'some question'}
        self.url = reverse('question-list') #urls.py에 정의된 urlpattern name

    def test_create_question(self):
        user =User.objects.create(username='testuser', password='testpass')
        # 클라이언트 강제 로그인 (APITestCase 상속 받은 이유)
        self.client.force_authenticate(user=user)
        # self.url로 post 요청
        response = self.client.post(self.url, self.question_data)
        # 응답 201번인지 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 생성된 객체가 1개인지 확인
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        # 내가 넣은 데이터가 맞는지 확인
        self.assertEqual(question.question_text, self.question_data['question_text'])
        # #1초 안에 동작하는지 테스트
        self.assertLess((timezone.now() - question.pub_date).total_seconds(), 1)
    
    #로그인 없이 post 요청은 안되어야함
    def test_create_question_without_authentication(self):
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_question(self):
        # Question 객체 2개 만들고 응답, 객체수, 생성객체 확인해보기
        question = Question.objects.create(question_text='Question1')
        choice = Choice.objects.create(question=question, choice_text='Choice1')
        Question.objects.create(question_text='Question2')
        response = self.client.get(self.url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['choices'][0]['choice_text'], choice.choice_text)


class VoteSerializerTest(TestCase):
    # test 실행시 setUp됨
    # test 만을 위한 별도의 database가 존재
    # 각 함수마다 1번 실행되고 함수 종료시 test 데이터베이스에서 만든 목록은 사라짐
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.question = Question.objects.create(
            question_text='abc',
            owner=self.user,
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text='1'
        )

    def test_vote_serializer(self):
        # 각 테스트 함수마다 setup이 만들어지고 함수 종료시 바로 사라짐.
        self.assertEqual(User.objects.all().count(), 1)
        data = {
            'question' : self.question.id,
            'choice' : self.choice.id,
            'voter' : self.user.id,
        }
        serializer = VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        vote = serializer.save()

        self.assertEqual(vote.question, self.question)
        self.assertEqual(vote.choice, self.choice)
        self.assertEqual(vote.voter, self.user)
    
    def test_vote_serializer_with_duplicate_vote(self):
        self.assertEqual(User.objects.all().count(), 1)
        data = {
            'question' : self.question.id,
            'choice' : self.choice.id,
            'voter' : self.id,
        }
        Vote.objects.create(question=self.question, choice=self.choice, voter=self.user)
        
        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid()) 

    def test_vote_serializer_with_numatched_question_and_choice(self):
        question2 = Question.objects.create(
            question_text = 'abc',
            owner=self.user,
        )
        choice2 = Choice.objects.create(
            question=question2,
            choice_text='1'
        )
        #question은 setup()에서 만든 질문
        #choice는 question2의 질문이므로 unmatch한 상황
        data = {
            'question' : self.question.id,
            'choice' : choice2.id,
            'voter' : self.user.id,
        }
        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class QuestionSerializerTestCase(TestCase):
    def test_with_valid_date(self):
        serializer = QuestionSerializer(data={'question_text' : 'abc'})
        self.assertEqual(serializer.is_valid(), True)
        new_question = serializer.save()
        self.assertIsNotNone(new_question.id)
        

    def test_with_invalid_date(self):
        serializer = QuestionSerializer(data={'question_text' : ''})
        self.assertEqual(serializer.is_valid(), False)