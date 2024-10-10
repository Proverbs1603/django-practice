from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

# Register your models here.

#StackedInline 은 세로방향 정렬
#TabularInline 은 가로방향 정렬
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  #3개의 추가할 빈 choice 입력칸이 default로 나옴.


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('question_text__', {'fields': ['question_text'], 'description': ['퀘스천']}),
        ('pub_data__', {'fields': ['pub_date'], 'classes': ['collapse']}),        
    ]
    readonly_fields = ['pub_date'] #읽기모드 *auto_now_add = True 조건이면.
    inlines = [ChoiceInline]

class ChoiceAdmin(admin.ModelAdmin):
    #한글필드명은 나오지 않고있음.
    fieldsets = [
        ('질문 텍스트', {
            'fields': ['choice_text']
            }),
        ('투표수', {
            'fields': ['votes'], 'description': ['투표수']
            })
    ]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)