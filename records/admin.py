from django.contrib import admin
from .models import Certification, StudyRecord

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(StudyRecord)
class StudyRecordAdmin(admin.ModelAdmin):
    list_display = ['date', 'certification', 'hours', 'user']  # ← 修正！
    list_filter = ['date', 'certification']
    search_fields = ['description']
    date_hierarchy = 'date'