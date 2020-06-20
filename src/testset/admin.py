from django.contrib import admin

# Register your models here.
from testset.models import Test, Question, Variant


class QuestionsInline(admin.TabularInline):
    model = Question
    fields = ('text',)  # 'num_variant_min_limit')
    show_change_link = True
    extra = 1


class TestAdminModel(admin.ModelAdmin):
    fields = ('title', 'description', 'level', 'image')
    list_display = ('title', 'description', 'level', 'image')
    list_per_page = 10
    inlines = (QuestionsInline,)


class VariantInline(admin.TabularInline):
    model = Variant
    fields = ('text',)  # 'num_variant_min_limit')
    show_change_link = True
    extra = 1


class QuestionsAdminModel(admin.ModelAdmin):
    model = Question
    fields = ('text',)  # 'num_variant_min_limit')
    show_change_link = True
    extra = 1
    inlines = (VariantInline,)


admin.site.register(Test, TestAdminModel)
admin.site.register(Question, QuestionsAdminModel)
