from django.contrib import admin
from .models import StudyRecord

@admin.register(StudyRecord)
class StudyRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'hours', 'created_at')
    list_filter = ('date',)
    search_fields = ('title', 'content')
    date_hierarchy = 'date'