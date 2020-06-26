from django.contrib import admin

# Register your models here.
from testset.forms import TestForm, QuestionsInlineFormSet, AnswerInlineFormSet
from testset.models import Test, Question, Variant


class QuestionsInline(admin.TabularInline):
    model = Question
    fields = ('text', 'number')  # 'num_variant_min_limit')
    show_change_link = True
    extra = 0
    formset = QuestionsInlineFormSet


class TestAdminModel(admin.ModelAdmin):
    fields = ('title', 'description', 'level', 'image')
    list_display = ('title', 'description', 'level', 'image')
    list_per_page = 10
    inlines = (QuestionsInline,)
    form = TestForm


class VariantInline(admin.TabularInline):
    model = Variant
    fields = ('text', 'is_correct')  # 'num_variant_min_limit')
    show_change_link = False
    extra = 0
    formset = AnswerInlineFormSet


class QuestionsAdminModel(admin.ModelAdmin):
    list_display = ('number', 'text', 'description', 'test')
    list_select_related = ('test',)
    list_per_page = 10
    search_fields = ('first_name',)
    inlines = (VariantInline,)


admin.site.register(Test, TestAdminModel)
admin.site.register(Question, QuestionsAdminModel)
