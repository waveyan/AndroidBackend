from django.contrib import admin

from evaluationapp.models import Evaluation, Comment


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['feeling', 'time','user']
    # list_filter=['created_time']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['word', 'time']


admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Comment, CommentAdmin)
